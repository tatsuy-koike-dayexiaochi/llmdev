from __future__ import annotations

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

from .state import GraphState
from .tools import build_tools

def _load_system_prompt() -> str:
    return (
        "あなたのキャラクターを設定します。北斗の拳のラオウです。"
    )

def build_graph(config) -> object:
    tools = build_tools(config)

    llm = ChatOpenAI(
        model=config["OPENAI_CHAT_MODEL"],
        api_key=config["OPENAI_API_KEY"],
        temperature=0,
    ).bind_tools(tools)

    system_prompt = _load_system_prompt()
    system_msg = SystemMessage(content=system_prompt)

    def agent(state: GraphState):
        msgs = [system_msg] + list(state["messages"])
        resp = llm.invoke(msgs)
        return {"messages": [resp]}

    graph = StateGraph(GraphState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
