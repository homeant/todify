from typing import Iterator, Union

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import BaseChatOpenAI

from app.llm._llm_api_client import LLMClient
from app.config.setting import settings


class SiliconFlowClient(LLMClient):

    def __init__(self):
        self.client = BaseChatOpenAI(
            openai_api_key=settings.silicon_flow_api_key,
            model_name=settings.silicon_flow_model,
            openai_api_base="https://api.siliconflow.cn/v1",
        )

    def text_chat(
        self, message: Union[str, list[str]], stream: bool = False
    ) -> Union[str, Iterator[str]]:
        prompt = ChatPromptTemplate.from_messages(message)
        chain = prompt | self.client
        return chain.invoke(input={}, stream=stream)
