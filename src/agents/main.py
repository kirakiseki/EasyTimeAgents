import streamlit as st
from langchain_core.messages import (
    HumanMessage,
    BaseMessage,
    SystemMessage,
    AIMessage,
    ToolMessage,
)

import utils
from graph.main_graph import get_main_graph
from utils.streamlit_callback import (
    get_streamlit_callback_handler,
    tool_call_inputs_renderer,
)
import utils.utils


def main():
    graph = get_main_graph(debug=True)

    # Recover session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_dataset" not in st.session_state:
        st.session_state.user_dataset = None

    for msg in st.session_state.messages:
        if isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)

            if msg.tool_calls:
                tool_call = msg.tool_calls[0]
                tool_container = st.empty()
                tool_status = tool_container.status("工具调用完成", expanded=True)

                with tool_status as s:
                    st.write("工具： ", tool_call["name"])
                    st.write("工具输入: ")
                    st.code(tool_call_inputs_renderer(tool_call["args"]))
                    st.write("工具输出: ")
                    tool_output_placeholder = st.empty()

        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        elif isinstance(msg, ToolMessage):
            if tool_output_placeholder:
                tool_output_placeholder.code(msg.content)

    with st.sidebar:
        st.header("📊 EasyTime - 多智能体系统")
        user_dataset = st.file_uploader(
            "上传时间序列数据集", type=["csv"], accept_multiple_files=False
        )

    # Execute every time the user interacts with the chat
    if prompt := st.chat_input(""):
        st.chat_message("user").write(prompt)
        st.session_state.user_dataset = utils.utils.copy_upload_file(user_dataset)

        with st.chat_message("ai"):
            st_callback_handler = get_streamlit_callback_handler(st.container())
            response = graph.invoke(
                input={
                    "messages": prompt,
                    "attachment": st.session_state.user_dataset,
                    "todo_subtasks": [],
                    "done_subtasks": [],
                },
                config={
                    "callbacks": [st_callback_handler],
                },
            )

        st.session_state.messages.extend(response["messages"])


if __name__ == "__main__":
    main()
