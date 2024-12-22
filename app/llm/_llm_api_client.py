from abc import ABC, abstractmethod
from typing import Iterator, Union


class LLMClient(ABC):
    @abstractmethod
    def text_chat(
        self, message: Union[str, list[str]], stream: bool = False
    ) -> Union[str, Iterator[str]]:
        """处理文本消息并返回LLM的文本响应。"""
        pass
