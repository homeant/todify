import logging

from app.rag.akshare_functions import AkShareFunctions

logger = logging.getLogger(__name__)


def test_ak_share_functions():
    res = AkShareFunctions().extract_akshare_functions()
    logger.info(f"res:{res}")
