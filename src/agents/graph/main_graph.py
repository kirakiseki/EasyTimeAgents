from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, START, END, add_messages
from typing import Annotated, Sequence, TypedDict
from langchain_core.runnables import Runnable
from langchain_core.language_models import BaseLanguageModel
from langgraph.checkpoint.memory import MemorySaver
from langchain_zhipu import ChatZhipuAI
from langchain_core.messages import (
    HumanMessage,
    BaseMessage,
    SystemMessage,
    AIMessage,
    ToolMessage,
)

import agents.models as models
import agents.agents as agents


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    attachment: str


lite_model = models.get_lite_llm()
plus_model = models.get_plus_llm()
vlm_model = models.get_vlm()

analyzer = agents.get_analyzer_agent(lite_model)


def analyzer_agent_node(state: GraphState):
    messages = state["messages"]
    attachment = state["attachment"]
    response = analyzer.invoke({"messages": messages, "attachment": attachment})

    return {"messages": [response]}


def get_main_graph(debug=True) -> CompiledStateGraph:
    graph = StateGraph(GraphState)
    graph.add_node("agent", analyzer_agent_node)
    graph.set_entry_point("agent")

    return graph.compile(debug=debug)
