import logging

from app.embeddings.embedding_factory import EmbeddingFactory

logger = logging.getLogger(__name__)


def test_factory():
    embeddings = EmbeddingFactory().get_instance("DashScopeEmbeddings")
    logger.info(embeddings.to_embeddings(["test"]))
