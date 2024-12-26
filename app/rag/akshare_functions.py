import inspect
import logging
from typing import Dict, List

import akshare as ak

from app.embeddings.embedding_factory import EmbeddingFactory
from app.config.setting import settings

logger = logging.getLogger(__name__)


class AkShareFunctions:
    def __init__(self):
        factory = EmbeddingFactory()
        self.embeddings = factory.get_instance(settings.embeddings_model_name)

    @classmethod
    def extract_akshare_functions(cls) -> List[Dict]:
        logger.info("正在从 akshare 库中提取函数...")
        functions = []
        for name, obj in inspect.getmembers(ak):
            if inspect.isfunction(obj):
                doc = inspect.getdoc(obj)
                if doc:
                    functions.append({"name": name, "docstring": doc})
        logger.info(f"已提取 {len(functions)} 个带有文档字符串的函数")
        return functions
