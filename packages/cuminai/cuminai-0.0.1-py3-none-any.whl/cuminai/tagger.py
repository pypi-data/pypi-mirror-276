import asyncio
from tqdm.asyncio import tqdm_asyncio

import cuminai.utils as utils

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped

class Tagger:
    def __init__(self, chunks, knowledge, **kwargs):
        self._chunks = chunks
        
        tags = dict()
        for source in knowledge:
            if hasattr(source, 'metadata') and 'tags' in source.metadata:
                tags[source.source] = [tag.lower() for tag in source.metadata['tags']]
            else:
                tags[source.source] = []
        
        self._tags = tags

    def add_global_tags(self):
        asyncio.run(self._tag_chunks_global())

    def add_local_tags(self, tag_threshold):
        asyncio.run(self._tag_chunks_local(tag_threshold))

    def get_tagged_chunks(self):
        return self._chunks
    
    async def _tag_chunks_global(self):
        tasks = [self._tag_chunk_global(chunk) for chunk in self._chunks]
        await tqdm_asyncio.gather(*tasks, desc="Tagging Knowledge", ascii=' >=')

    @background
    def _tag_chunk_global(self, chunk):
        for tag in self._tags[chunk.metadata['source']]:
            chunk.metadata[f'tag-{utils.get_processed_tag(tag)}'] = True
    
    async def _tag_chunks_local(self, tag_threshold):
        tasks = [self._tag_chunk_local(chunk, tag_threshold) for chunk in self._chunks]
        await tqdm_asyncio.gather(*tasks, desc="Tagging Knowledge", ascii=' >=')
    
    @background
    def _tag_chunk_local(self, chunk, tag_threshold):
        for tag in self._tags[chunk.metadata['source']]:
            if utils.num_found(chunk.page_content, tag) >= tag_threshold:
                chunk.metadata[f'tag-{utils.get_processed_tag(tag)}'] = True