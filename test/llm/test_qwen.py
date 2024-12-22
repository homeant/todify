import logging

from app.llm.qwen_client import QwenClient

logger = logging.getLogger(__name__)


def test_qwen_client():
    client = QwenClient()
    res = client.text_chat("你好")
    logger.info(f"res:{res}")
