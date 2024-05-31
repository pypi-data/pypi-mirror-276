import re

from cuminai.constants import (
    _LINK_KIND,
    _TEXT_KIND,
    _PUBLIC_VISIBILITY,
    _PRIVATE_VISIBILITY,
    _GLOBAL_TAGGING,
    _LOCAL_TAGGING,
)

from cuminai.config import ChunkStrategy, Tag, KnowledgeSource, Version
import cuminai.utils as utils

UsernameValidator = re.compile('^[0-9a-zA-Z]{6,36}$')
NameValidator = re.compile('^[0-9a-zA-Z]+$')

OllamaEmbeddingValidator = re.compile('^ollama/(mxbai-embed-large|nomic-embed-text|all-minilm)(latest|(:v[0-9a-zA-Z-_.]+))?$')

LinkValidator = re.compile('^(https://www.|https://)[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?/[a-zA-Z0-9]{2,}|((https://www.|https://)[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?)|(https://www.|https://)[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}(.[a-zA-Z0-9]{2,})?$')
TextFileValidator = re.compile('^.+(.txt|.md)$')

OllamaEmbeddingFetcher = re.compile('^ollama/(.*)$')
KbVersionFetcher = re.compile('^(@[0-9a-zA-Z]{6,36}/[0-9a-zA-Z]+)(|:([0-9a-zA-Z_-]+))$')

class Validator:
    def __init__(self, cuminfile, **kwargs):
        self._cuminfile = cuminfile
    
    def validate(self):
        if not hasattr(self._cuminfile, 'name') or \
            not NameValidator.match(self._cuminfile.name):
            raise ValueError("::invalid name field: 'name' is required field and should be non empty alphanumeric string without spaces and symbols")
        
        if not hasattr(self._cuminfile, 'kind') or \
            self._cuminfile.kind not in [_LINK_KIND, _TEXT_KIND]:
            raise ValueError(f"::invalid kind: 'kind' is required and its value should be [{_LINK_KIND}|{_TEXT_KIND}]")
        
        if not hasattr(self._cuminfile, 'version') or \
            not isinstance(self._cuminfile.version, dict):
            raise ValueError("::invalid version: 'version' is required and should be a dict containing tag")

        self._cuminfile.version = Version(**self._cuminfile.version)

        if not hasattr(self._cuminfile.version, 'tag') or \
            not isinstance(self._cuminfile.version.tag, str) or \
                not self._cuminfile.version.tag:
            raise ValueError("::invalid version:tag: tag should be non empty string")
        
        if hasattr(self._cuminfile.version, 'latest'):
            if not isinstance(self._cuminfile.version.latest, bool):
                raise ValueError("::invalid version:latest: latest version tag should be [true|false] default: false")
        
        if not hasattr(self._cuminfile, 'type') and \
            self._cuminfile.type not in [_PUBLIC_VISIBILITY, _PRIVATE_VISIBILITY]:
            raise ValueError(f"::invalid type: 'type' is an optional field, but if defined, its value should be [{_PUBLIC_VISIBILITY}|{_PRIVATE_VISIBILITY}]. default: {_PRIVATE_VISIBILITY}")
        
        if not hasattr(self._cuminfile, 'embedding') or \
            not isinstance(self._cuminfile.embedding, str) or \
            not OllamaEmbeddingValidator.match(self._cuminfile.embedding):
            raise ValueError("::invalid embedding: 'embedding' is required, its value should be a valid ollama embedding name like 'ollama/nomic-embed-text:v1.5'")
        
        if hasattr(self._cuminfile, 'tag'):
            if not isinstance(self._cuminfile.tag, dict):
                raise ValueError(f"::invalid tag: 'tag' is required")
        
            self._cuminfile.tag = Tag(**self._cuminfile.tag)
            if self._cuminfile.tag.type not in [_GLOBAL_TAGGING, _LOCAL_TAGGING]:
                raise ValueError(f"::invalid tag:type: tag type should be [{_GLOBAL_TAGGING}|{_LOCAL_TAGGING}]")

            if self._cuminfile.tag.type == _LOCAL_TAGGING:
                if not hasattr(self._cuminfile.tag, 'minoccurances') or \
                    not isinstance(self._cuminfile.tag.minoccurances, int) or \
                    self._cuminfile.tag.minoccurances < 0:
                    raise ValueError(f"::invalid tag:type:local: local tag must have valid minoccurances field value")

        if not hasattr(self._cuminfile, 'knowledge') or \
            not isinstance(self._cuminfile.knowledge, list):
            raise ValueError("::invalid knowledge source: 'knowledge' is required, and should be a list of knowledge sources")
        
        self._cuminfile.knowledge = [KnowledgeSource(**source) for source in self._cuminfile.knowledge]

        if any(not hasattr(sourcedetails, 'source') for sourcedetails in self._cuminfile.knowledge) or \
            any(not utils.isValidKnowledgeSource(sourcedetails, self._cuminfile.kind) 
                for sourcedetails in self._cuminfile.knowledge):
            raise ValueError(f"::invalid knowledge->source: 'knowledge' source is not of valid kind {self._cuminfile.kind}")

        if any(hasattr(source, 'metadata') and 'tags' in source.metadata and  \
            not isinstance(source.metadata['tags'], list) \
                for source in self._cuminfile.knowledge):
            raise ValueError("::invalid knowledge:metadata:tags: metadata tags should be a list")

        if any(hasattr(source, 'metadata') and \
               'tags' in source.metadata and \
                any(not isinstance(tag, str) or not tag for tag in source.metadata['tags']) 
                for source in self._cuminfile.knowledge):
            raise ValueError("::invalid knowledge:metadata:tags: metadata tags should be a list of non-empty string tags")
        
        if hasattr(self._cuminfile, 'chunkstrategy') and \
            not isinstance(self._cuminfile.chunkstrategy, dict):
            raise ValueError("::invalid chunkstrategy: chunk strategy is optional, but if defined, must be a dict containing size and overlap")
        
        if hasattr(self._cuminfile, 'chunkstrategy'):
            self._cuminfile.chunkstrategy = ChunkStrategy(**self._cuminfile.chunkstrategy)
            if not hasattr(self._cuminfile.chunkstrategy, 'size') or \
                not isinstance(self._cuminfile.chunkstrategy.size, int) or \
                self._cuminfile.chunkstrategy.size < 100 or self._cuminfile.chunkstrategy.size > 8196:
                raise ValueError("::invalid chunkstrategy:size: size should be a positive integer value (min:100, max:8196)")
            
            if not hasattr(self._cuminfile.chunkstrategy, 'overlap') or \
                not isinstance(self._cuminfile.chunkstrategy.overlap, int) or \
                self._cuminfile.chunkstrategy.overlap < 0 or \
                    self._cuminfile.chunkstrategy.overlap > self._cuminfile.chunkstrategy.size/2:
                raise ValueError("::invalid chunkstrategy:overlap: overlap should be a non negative integer value (min:0, max:val[size]/2)")
            
    def get_cuminfile(self):
        return self._cuminfile