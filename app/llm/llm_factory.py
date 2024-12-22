from app.core.factory import Factory
from app.core.singleton import Singleton
from app.llm._llm_api_client import LLMClient


class LLMFactory(Factory[LLMClient], metaclass=Singleton):

    def __init__(self):
        super().__init__(r"class\s+(\w+)\s*\([^)]*Client[^)]*\):")
