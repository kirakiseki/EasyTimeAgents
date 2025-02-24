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
import utils.utils


def main():
    graph = get_main_graph(debug=False)

    # Recover session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_dataset" not in st.session_state:
        st.session_state.user_dataset = None

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

    # Execute every time the user interacts with the chat
    if prompt := st.chat_input(""):
        st.chat_message("user").write(prompt)

        # If user dataset is uploaded at first time, copy it to upload dir and save it to session state
        if st.session_state.user_dataset is None:
            st.session_state.user_dataset = utils.utils.copy_upload_file(user_dataset)

        with st.chat_message("ai"):
            st_callback_handler = get_streamlit_callback_handler(st.container())
            response = graph.invoke(
                input={"messages": prompt, "attachment": st.session_state.user_dataset},
                config={
                    "callbacks": [st_callback_handler],
                },
            )

            st.session_state.messages.extend(response["messages"])


if __name__ == "__main__":
    main()
