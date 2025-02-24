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
from utils import CONFIG

class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    attachment: str
    
# == DEMO
def call_model(state: GraphState):
    messages = state["messages"]
    model = ChatZhipuAI(model=CONFIG['models']['zhipuai']['llm_model'], temperature=CONFIG['models']['zhipuai']['temperature'], streaming=True)
    response = model.invoke(messages)

    return {"messages": [response]}
# == END DEMO

def get_main_graph(debug=True) -> CompiledStateGraph:
    graph = StateGraph(GraphState)
    graph.add_node("agent", call_model)
    graph.set_entry_point("agent")

    return graph.compile(debug=debug)