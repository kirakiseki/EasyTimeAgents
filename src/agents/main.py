import streamlit as st

import utils
from graph.main_graph import get_main_graph
from utils.streamlit_callback import get_streamlit_callback_handler

def main():
    graph = get_main_graph(debug=False)
    st.session_state.messages = []
    
    for msg in st.session_state.messages:
        match msg.get("type"):
            case "chat":
                st.chat_message("ai").write(msg.get("content"))
            case _:
                pass
            
    
    with st.sidebar:
        st.header("📊 EasyTime - 多智能体系统")
        user_dataset = st.file_uploader("上传时间序列数据集", type=['csv'], accept_multiple_files=False)
        
    if prompt := st.chat_input(""):
        st.chat_message("user").write(prompt)
        
        with st.chat_message("ai"):
            st_callbackHandler = get_streamlit_callback_handler(st.container())
            graph.invoke(
                {
                    "messages": prompt,
                },
                config={
                    "callbacks": [st_callbackHandler],
                },
            )

if __name__ == '__main__':
    main()