from langchain_core.language_models import BaseChatModel
from langchain_openai.chat_models.base import BaseChatOpenAI

from app.config.setting import settings
from app.core.singleton import Singleton

MODEL_NAME_MAPPING = {
    "Qwen2.5-32B-Instruct": {
        "model_name": "Qwen/Qwen2.5-32B-Instruct",
        "openai_api_base": "https://api.siliconflow.cn/v1",
        "openai_api_key": settings.silicon_flow_api_key,
    }
}


class LLMFactory(metaclass=Singleton):

    @classmethod
    def get_client(cls, model_name: str) -> BaseChatModel:
        if model_name in MODEL_NAME_MAPPING:
            config = MODEL_NAME_MAPPING[model_name]
            return BaseChatOpenAI(**config)
        else:
            raise ValueError(f"Unsupported model name: {model_name}")
