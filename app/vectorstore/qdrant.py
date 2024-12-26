import logging
from typing import Iterable, List, Optional, Sequence

from langchain_community import embeddings
from langchain_qdrant import QdrantVectorStore as Lc_QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.config.setting import settings
from app.vectorstore._vectorstore import VectorStore

logger = logging.getLogger(__name__)


class QdrantVectorStore(VectorStore):
    def __init__(self, collection_name: str):
        client = QdrantClient(
            location=settings.qdrant_url, api_key=settings.qdrant_api_key, timeout=60
        )
        try:
            client.get_collection(collection_name=collection_name)
        except Exception:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
            logger.info(f"Collection {collection_name} created")
        self._store = Lc_QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings.DashScopeEmbeddings(
                model=settings.embeddings_model_name,
                dashscope_api_key=settings.dash_scope_api_key,
            ),
        )
        self._collection_name = collection_name

    def add_texts(
        self,
        texts: Iterable[str],
        meta_datas: Optional[List[dict]] = None,
        ids: Optional[Sequence[str | int]] = None,
    ):
        self._store.add_texts(
            texts=texts,
            metadatas=meta_datas,
            ids=ids,
        )

    def search(self, text: str, k: int = 4) -> List[dict]:
        return self._store.similarity_search(text, k=k)
