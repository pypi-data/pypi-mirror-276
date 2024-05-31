import asyncio
from tqdm.asyncio import tqdm_asyncio

from cuminai.constants import (
    _DEFAULT_CHUNK_SIZE,
    _DEFAULT_CHUNK_OVERLAP,
)

from langchain_text_splitters import CharacterTextSplitter

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped

class Chunker:
    def __init__(self, docs, **kwargs):
        self._docs = docs
        self._chunk_size = kwargs.get('chunk_size', _DEFAULT_CHUNK_SIZE)
        self._chunk_overlap = kwargs.get('chunk_overlap', _DEFAULT_CHUNK_OVERLAP)

    def get_chunks(self):
        return asyncio.run(self._aget_chunks())
    
    async def _aget_chunks(self):
        chunkset = [self._aget_chunk_for_doc(doc) for doc in self._docs]
        chunks = [chunk for doc_chunks in await tqdm_asyncio.gather(*chunkset, desc="Chunking Knowledge", ascii=' >=') for chunk in doc_chunks]
        return chunks
    
    @background
    def _aget_chunk_for_doc(self, doc):
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self._chunk_size, chunk_overlap=self._chunk_overlap
        )

        return text_splitter.split_documents([doc])

