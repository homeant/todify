from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState, _validate_chat_history


def call_model(
    runnable: Runnable, state: AgentState, config: RunnableConfig
) -> AgentState:
    _validate_chat_history(state["messages"])
    response = runnable.invoke(state, config)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


async def acall_model(
    runnable: Runnable, state: AgentState, config: RunnableConfig
) -> AgentState:
    _validate_chat_history(state["messages"])
    response = await runnable.ainvoke(state, config)
    return {"messages": [response]}
