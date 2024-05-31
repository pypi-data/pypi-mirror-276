from tqdm.asyncio import tqdm_asyncio
from typing import List
from langchain_community.embeddings import OllamaEmbeddings
import asyncio

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped

class CuminAIEmbeddings(OllamaEmbeddings):
    def _embed(self, input: List[str]) -> List[List[float]]:
        return asyncio.run(self._embed_prompts(input))

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        instruction_pairs = [f"{self.embed_instruction}{text}" for text in texts]
        embeddings = self._embed(instruction_pairs)
        return embeddings
    
    async def _embed_prompts(self, prompts):
        embeddings = [self._aembed_prompt(prompt) for prompt in prompts]
        return await tqdm_asyncio.gather(*embeddings, desc="Embedding Knowledge", ascii=' >=', leave=False, nrows=20)

    @background
    def _aembed_prompt(self, prompt):
        return self._process_emb_response(prompt)