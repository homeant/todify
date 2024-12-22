from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(description="消息的角色")
    content: str = Field(description="消息内容")


class ChatCompletionRequest(BaseModel):
    model: str = Field(description="使用的模型名称")
    messages: List[Message] = Field(description="对话历史")
    stream: bool = Field(default=False, description="是否使用流式响应")
    temperature: Optional[float] = Field(
        default=0.7, description="温度参数", ge=0, le=2
    )


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Literal["stop", "length", "content_filter", "null"] = "stop"


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletionResponse(BaseModel):
    id: str = Field(description="响应ID")
    object: str = "chat.completion"
    created: int = Field(description="创建时间戳")
    model: str = Field(description="使用的模型")
    choices: List[Choice]
    usage: Usage
