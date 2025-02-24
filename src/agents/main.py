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
from utils.streamlit_callback import get_streamlit_callback_handler


def main():
    graph = get_main_graph(debug=False)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        if isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)

    with st.sidebar:
        st.header("📊 EasyTime - 多智能体系统")
        user_dataset = st.file_uploader(
            "上传时间序列数据集", type=["csv"], accept_multiple_files=False
        )

    if prompt := st.chat_input(""):
        st.chat_message("user").write(prompt)

        with st.chat_message("ai"):
            st_callbackHandler = get_streamlit_callback_handler(st.container())
            response = graph.invoke(
                {
                    "messages": prompt,
                },
                config={
                    "callbacks": [st_callbackHandler],
                },
            )

            st.session_state.messages.extend(response["messages"])


if __name__ == "__main__":
    main()
