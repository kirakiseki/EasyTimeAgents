from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, START, END, add_messages
from typing import Annotated, Sequence, TypedDict, List
from langgraph.prebuilt import ToolNode
from langchain_core.messages import (
    HumanMessage,
    BaseMessage,
    SystemMessage,
    AIMessage,
    ToolMessage,
)
import uuid
import re

import agents.models as models
import agents.agents as agents
import tools.jupyter
import tools.characteristic_extractor
import tools.timeseries_format_checker

all_tools = [
    tools.timeseries_format_checker.TimeSeriesFormatCheckerTool(),
    tools.jupyter.JupyterNotebook(),
    tools.characteristic_extractor.TimeSeriesCharacteristicsExtractorTool(),
]


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    attachment: str
    current_node: str
    todo_subtasks: List[str]
    done_subtasks: List[str]
    current_subtask: str


lite_model = models.get_lite_llm()
plus_model = models.get_plus_llm()
vlm_model = models.get_vlm()

greeting_agent = agents.get_greeting_agent(lite_model)


def greeting_agent_node(state: GraphState):
    state["current_node"] = "greeting_agent"

    messages = state["messages"]
    attachment = state["attachment"]
    response = greeting_agent.invoke({"messages": messages, "attachment": attachment})
    response.tool_calls = [
        {
            "name": "时间序列数据格式检查器",
            "args": {
                "file_path": attachment,
            },
            "id": str(uuid.uuid4()),
        }
    ]

    return {"messages": [response]}


def greeting_router(state: GraphState):
    messages = state["messages"]
    last_message = messages[-1]

    if state["attachment"] == "NO_UPLOAD_FILE":
        return END

    if last_message.tool_calls:
        return "checker_tools"


checker_tools = [tools.timeseries_format_checker.TimeSeriesFormatCheckerTool()]
checker_tools_node = ToolNode(checker_tools)

checker_agent = agents.get_checker_agent(plus_model)


def checker_agent_node(state: GraphState):
    state["current_node"] = "checker_agent"

    messages = state["messages"]
    attachment = state["attachment"]

    response = checker_agent.invoke({"messages": messages, "attachment": attachment})

    return {"messages": [response]}


decomposer_agent = agents.get_decomposer_agent(plus_model)


def decomposer_agent_node(state: GraphState):
    state["current_node"] = "decomposer_agent"

    messages = state["messages"]
    attachment = state["attachment"]
    done_subtasks = state["done_subtasks"]
    done_subtasks_str = (
        "None" if len(done_subtasks) == 0 else "\n - ".join(done_subtasks)
    )

    response = decomposer_agent.invoke(
        {
            "messages": messages,
            "attachment": attachment,
            "done_subtasks": done_subtasks_str,
        }
    )

    last_content = response.content

    task_block = re.search(r"```tasks\n(.*?)\n```", last_content, re.DOTALL)

    if task_block:
        task_list = [
            line.replace("- ", "", 1).strip()
            for line in task_block.group(1).split("\n")
            if line.strip()
        ]

    else:
        task_list = []

    return {"messages": [response], "todo_subtasks": task_list}


def get_main_graph(debug=True) -> CompiledStateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("greeting_agent", greeting_agent_node)
    graph.add_node("checker_tools", checker_tools_node)
    graph.add_node("checker_agent", checker_agent_node)
    graph.add_node("decomposer_agent", decomposer_agent_node)

    # START -> greeting_agent -> checker_tools -> checker_agent -> decomposer_agent
    graph.add_edge(START, "greeting_agent")
    graph.add_conditional_edges("greeting_agent", greeting_router)
    graph.add_edge("checker_tools", "checker_agent")
    graph.add_edge("checker_agent", "decomposer_agent")

    # DEBUG
    graph.add_edge("decomposer_agent", END)

    return graph.compile(debug=debug)
