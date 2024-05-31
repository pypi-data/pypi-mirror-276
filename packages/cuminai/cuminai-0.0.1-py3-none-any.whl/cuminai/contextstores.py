import os
from typing import (
    Any, 
    Optional
)

import qdrant_client
from qdrant_client import models
from langchain_qdrant import Qdrant
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.embeddings import Embeddings
from cuminai.constants import (
    _CUMINAI_DUMMY_COLLECTION_NAME,
    _CUMINAI_API_KEY_ENV,
    _CUMINAI_HOST,
)
from cuminai.validator import KbVersionFetcher
class CuminAI:
    """`Cumin AI context store

    To use, you should have the ``qdrant_client`` python package and ``langchain_qdrant`` python package installed.

    Example:
        .. code-block:: python

                from cuminai import CuminAI

                embeddings = OpenAIEmbeddings()
                contextsource = CuminAI("cuminai_source", embeddings)
    """

    def __init__(
            self,
            source: str,
            embedding_function: Optional[Embeddings] = None
    ) -> None:
        """Initialize with a Cumin AI client"""
        if source is None:
            raise ValueError("No context source present.")
        api_key = os.getenv(_CUMINAI_API_KEY_ENV)
        if api_key is None:
            raise ValueError("Cumin AI api key not set in env.")
        
        self._embedding_function = embedding_function

        match = KbVersionFetcher.match(source)
        if match is None:
            raise ValueError("invalid source format")
        kbAlias = match.groups()[0]
        if match.groups()[2] is None:
            kbVersion = "latest"
        else:
            kbVersion = match.groups()[2]

        try:
            self._client = qdrant_client.QdrantClient(
                url=_CUMINAI_HOST, 
                port=443,
                https=True,
                metadata={
                    "CUMINAI-API-KEY": api_key,
                    "CUMINAI-ALIAS": kbAlias,
                    "CUMINAI-KB-VERSION": kbVersion
                }
            )
        except ValueError:
            raise ValueError(f"Could not connect to {source}. Please make sure the source exists or the Cumin AI API key is valid.")

    def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        store = Qdrant(
            client=self._client,
            collection_name=_CUMINAI_DUMMY_COLLECTION_NAME,
            embeddings=self._embedding_function,
        )

        search_kwargs = kwargs.pop("search_kwargs", {})
        
        tags = search_kwargs.pop("cuminai_tags", None)

        if tags is not None:
            should_filters = [models.FieldCondition(key=f'metadata.tag-{tag.lower().replace("-","_").replace(" ", "_")}', match=models.MatchValue(value=True)) for tag in tags]
            filter = models.Filter(
                should=should_filters
            )
            search_kwargs["filter"] = filter   
            
        return store.as_retriever(**kwargs, search_kwargs=search_kwargs)