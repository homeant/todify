from typing import Iterator, Union

from langchain_openai.chat_models.base import BaseChatOpenAI

from app.llm._llm_api_client import LLMClient
from app.setting import settings


class QwenClient(LLMClient):

    def __init__(self):
        self.client = BaseChatOpenAI(
            openai_api_key=settings.dash_scope_api_key,
            model_name=settings.qwen_default_model,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    def text_chat(
        self, message: Union[str, list[str]], stream: bool = False
    ) -> Union[str, Iterator[str]]:
        return self.client.invoke(message, stream=stream)
