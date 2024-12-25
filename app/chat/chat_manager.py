import json
import logging
import uuid
from typing import AsyncGenerator, Literal

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_openai.chat_models.base import BaseChatOpenAI
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.managed import IsLastStep

from app.chat.schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    Message,
    Usage,
)
from app.chat.stock_workflow import StockWorkflow
from app.core.singleton import Singleton
from app.setting import settings
from app.tools.tool_manager import ToolManager
from app.utils.date import format_now, get_now_millis

logger = logging.getLogger(__name__)


class State(MessagesState):
    category: str
    is_last_step: IsLastStep


class ChatManager(metaclass=Singleton):
    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager
        self.agent_model = self._init_agent_model()
        self.stock_workflow = StockWorkflow(tool_manager)

    @classmethod
    def _init_agent_model(cls) -> BaseChatOpenAI:
        return BaseChatOpenAI(
            model_name="Qwen/Qwen2.5-32B-Instruct",
            openai_api_base="https://api.siliconflow.cn/v1",
            openai_api_key=settings.silicon_flow_api_key,
            temperature=0,
            verbose=True,
        )

    def get_work_flow(self) -> CompiledGraph:
        def categorize(state: State) -> State:
            """Categorize the customer query into Technical, Billing, or General."""
            prompt = ChatPromptTemplate.from_template(
                "根据用户问题，给出对应的分类，你只需要输出结果:"
                "Stock, General. \n Messages: {messages}"
            )
            chain = prompt | self.agent_model
            category = chain.invoke({"messages": state["messages"]}).content
            state["category"] = category
            return state

        def default_handler(state: State) -> State:
            prompt = ChatPromptTemplate.from_template(
                "你是一个智能助手，需要分析用户提出的问题，并给出合适的回答。\n Messages: {messages}"
            )
            chain = prompt | self.agent_model
            response = chain.invoke({"messages": state["messages"]})
            state["messages"] = [response]
            return state

        stock_workflow = self.stock_workflow.get_stock_graph()

        # tools = [
        #     stock_lhb_hyyyb_em,
        #     stock_lhb_detail_em
        # ]
        # stock_workflow = create_react_agent(self.agent_model, tools=tools, state_schema=State, debug=True, state_modifier="请根据用户问题，选择不同的工具，解决用户的问题")
        builder = StateGraph(State)
        builder.add_node("switch_agent", categorize)
        builder.add_node("stock_agent", stock_workflow)
        builder.add_node("default_handler", default_handler)
        builder.add_conditional_edges(
            "switch_agent",
            lambda state: (
                "stock_agent" if state["category"] == "Stock" else "default_handler"
            ),
            {
                "stock_agent": "stock_agent",
                "default_handler": "default_handler",
            },
        )
        builder.add_edge("stock_agent", "default_handler")
        builder.set_entry_point("switch_agent")
        builder.set_finish_point("default_handler")
        workflow = builder.compile(
            debug=True,
        )
        # byte_buffer = io.BytesIO(workflow.get_graph().draw_mermaid_png())
        # image = Image.open(byte_buffer)
        # image.show()
        return workflow

    @classmethod
    def _extract_usage(cls, message) -> Usage:
        """从LangChain消息中提取usage信息"""
        try:
            if hasattr(message, "additional_kwargs"):
                usage_data = message.additional_kwargs.get("usage", {})
                return Usage(
                    prompt_tokens=usage_data.get("prompt_tokens", 0),
                    completion_tokens=usage_data.get("completion_tokens", 0),
                    total_tokens=usage_data.get("total_tokens", 0),
                )
        except Exception as e:
            logger.warning(f"Failed to extract usage info: {e}")
        return Usage()

    async def handle_completion(
        self, request: ChatCompletionRequest
    ) -> ChatCompletionResponse | AsyncGenerator:
        inputs = {
            "messages": [self._format_message(request.messages[-1])],
            "today": format_now(),
        }
        workflow = self.get_work_flow()
        if request.stream:
            return self._handle_stream_completion(workflow, request, inputs)
        return await self._handle_sync_completion(workflow, request, inputs)

    async def _handle_sync_completion(
        self, workflow: CompiledGraph, request: ChatCompletionRequest, inputs: dict
    ):
        result = await workflow.ainvoke(inputs)
        final_message = result["messages"][-1]
        content = (
            final_message[1]
            if isinstance(final_message, tuple)
            else final_message.content
        )
        usage = self._extract_usage(final_message)

        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4()}",
            created=get_now_millis(),
            model=request.model,
            choices=[
                Choice(index=0, message=Message(role="assistant", content=content))
            ],
            usage=usage,
        )

    @classmethod
    def _create_stream_response(
        cls,
        message: BaseMessage,
        index: int = 0,
    ) -> dict:
        """创建符合OpenAI格式的流式响应"""
        return {
            "id": f"{message.id}",
            "object": "chat.completion.chunk",
            "created": get_now_millis(),
            "model": "Qwen2.5-32B-Instruct",
            "system_fingerprint": "fp_qwen25",
            "choices": [
                {
                    "index": index,
                    "delta": {"content": f"{message.content}\n\n"},
                    "logprobs": None,
                    "finish_reason": (
                        message.response_metadata.get("finish_reason")
                        if hasattr(message, "response_metadata")
                        else None
                    ),
                }
            ],
            "usage": (
                message.usage_metadata if hasattr(message, "usage_metadata") else None
            ),
        }

    async def _handle_stream_completion(
        self, workflow: CompiledGraph, request: ChatCompletionRequest, inputs: dict
    ):
        async for stream_res in workflow.astream(inputs):
            for message_type in stream_res.keys():
                body = stream_res.get(message_type)
                if body:
                    for index, message in enumerate(body.get("messages")):
                        # 使用新的响应格式
                        chunk_response = self._create_stream_response(
                            message=message,
                            index=index,
                        )
                        yield f"data: {json.dumps(chunk_response)}\n\n"

        # # 发送结束标记，带有finish_reason
        # final_chunk = self._create_stream_response(
        #     content="",
        #     index=0,
        #     finish_reason="stop"
        # )
        # yield f"data: {json.dumps(final_chunk)}\n\n"
        # yield "data: [DONE]\n\n"

    @classmethod
    def _get_usage(cls, usage: Usage, message: AIMessage) -> Usage:
        """从LangChain消息中提取usage信息"""
        usage.prompt_tokens += message.usage_metadata.get("prompt_tokens")
        usage.completion_tokens += message.usage_metadata.get("completion_tokens")
        usage.total_tokens += message.usage_metadata.get("total_tokens")
        return usage

    @classmethod
    def _format_message(
        cls, message: Message
    ) -> tuple[Literal["system", "user", "assistant"], str]:
        return message.role, message.content

    def get_tools(self, tool_type) -> list[Tool]:
        pass
