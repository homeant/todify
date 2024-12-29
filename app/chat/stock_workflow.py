import logging
from typing import List, Optional

from langchain_core.language_models import BaseChatModel, LanguageModelInput
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import Tool
from langchain_openai.chat_models.base import BaseChatOpenAI, _DictOrPydanticClass
from langgraph.graph import StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.utils.runnable import RunnableCallable
from pydantic import BaseModel, Field

from app.chat._workflow import acall_model
from app.config.setting import settings
from app.core.singleton import Singleton
from app.stock.trade_calendar import TradeCalendar
from app.tools.tool_manager import ToolManager
from app.utils.date import SIMPLE_FORMAT, date_format, now_format

logger = logging.getLogger(__name__)

STOCK_PROMPT = """你是一个专业的股票分析师，你能根据用户提出的问题，通过提供给你的工具帮助用户解决问题，并给出权威的总结。

今天是{today}，最后交易日是{last_trade_date}"""


class Keywords(BaseModel):
    """Answer with at least 5 keywords that you think are related to the topic"""

    keys: list = Field(description="list of at least 5 keywords related to the topic")


class StockState(AgentState):
    today: str
    last_trade_date: str
    keywords: list[str]


class StockWorkflow(metaclass=Singleton):
    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager
        self.trade_calendar = TradeCalendar()

    @classmethod
    def _get_model(
        cls,
        tools: List[Tool] = None,
        schema: Optional[_DictOrPydanticClass] = None,
    ) -> Runnable[LanguageModelInput, BaseMessage] | BaseChatModel:
        model = BaseChatOpenAI(
            model_name="Qwen/Qwen2.5-32B-Instruct",
            openai_api_base="https://api.siliconflow.cn/v1",
            openai_api_key=settings.silicon_flow_api_key,
            temperature=0,
            verbose=True,
        )
        if tools:
            return model.bind_tools(tools=tools)
        elif schema:
            return model.with_structured_output(schema)
        return model

    async def _agent_handler(
        self, state: StockState, config: RunnableConfig
    ) -> AgentState:
        model = self._get_model()
        return await acall_model(model, state, config)

    def get_stock_graph(self) -> CompiledGraph:
        workflow = StateGraph(StockState)
        workflow.add_node("keywords_agent", self._get_keywords)
        workflow.add_node("agent", RunnableCallable(self._agent_handler))
        workflow.add_node("choose_tool_agent", self._choose_tool)
        workflow.add_node("call_tool_agent", self._call_tool)
        workflow.add_edge("keywords_agent", "choose_tool_agent")
        workflow.add_conditional_edges("choose_tool_agent", self._router_choose_tool)

        workflow.set_entry_point("keywords_agent")

        return workflow.compile(debug=True)

    @classmethod
    def _router_choose_tool(cls, state: StockState, config: RunnableConfig) -> str:
        message = state.get("messages")[-1]
        if isinstance(message, AIMessage) and message.tool_calls:
            return "call_tool_agent"
        return "__end__"

    def _call_tool(self, state: StockState, config: RunnableConfig) -> StockState:
        message = state.get("messages")[-1]
        tools = []
        for call in message.tool_calls:
            tool = self.tool_manager.get_tool("akshare", call["name"])
            if tool:
                tools.append(tool)
        return ToolNode(tools).invoke({"messages": state["messages"]}, config)

    def _choose_tool(self, state: StockState, config: RunnableConfig) -> StockState:
        tools = self.tool_manager.search_and_create_tools(state["keywords"])
        prompt = ChatPromptTemplate.from_messages(
            [STOCK_PROMPT, ("placeholder", "{messages}")]
        )
        runnable = prompt | self._get_model(tools=tools)
        response = runnable.invoke(
            {
                "messages": state["messages"],
                "today": now_format(SIMPLE_FORMAT),
                "last_trade_date": date_format(
                    self.trade_calendar.get_last_trade_day(), SIMPLE_FORMAT
                ),
            }
        )
        return {"messages": [response]}

    def _get_keywords(self, state: StockState):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="你的任务是根据用户输入的问题，分析应该使用 akshare 哪些工具，提供5个关键词"
                ),
                ("placeholder", "{messages}"),
            ]
        )
        runnable = prompt | self._get_model(schema=Keywords)
        message = runnable.invoke({"messages": state["messages"]})
        return {"keywords": message.keys}
