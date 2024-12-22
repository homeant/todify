import logging
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import BaseChatOpenAI
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from langgraph.prebuilt import create_react_agent

from app.stock import lhb

logger = logging.getLogger(__name__)


class CustomState(TypedDict):
    today: str
    messages: Annotated[list[BaseMessage], add_messages]
    is_last_step: IsLastStep


def test_llm_agent():
    model = BaseChatOpenAI(
        model_name="Qwen/Qwen2.5-32B-Instruct",
        openai_api_base="https://api.siliconflow.cn/v1",
        openai_api_key="sk-xiqvdfobxlettkmqbhchyhxwjyfqgxsaimuseqomokhuszuh",
        temperature=0,
        verbose=True,
    )
    tools = [
        lhb.stock_lhb_hyyyb_em,
        lhb.stock_lhb_jgstatistic_em,
        lhb.stock_lhb_stock_statistic_em,
        lhb.stock_lhb_detail_em,
        lhb.stock_lhb_jgmmtj_em,
    ]
    model = model.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "今天是{today}， 你需要分析用户提出的问题，并选择合适的工具，最后对工具的结果进行总结",
            ),
            ("placeholder", "{messages}"),
        ]
    )

    graph = create_react_agent(
        model, tools, state_schema=CustomState, state_modifier=prompt
    )
    inputs = {"messages": [("user", "今日龙虎榜")], "today": "2024-12-20 18:40:20"}
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
