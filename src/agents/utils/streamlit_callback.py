import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from langchain_core.callbacks.base import BaseCallbackHandler
from typing import Dict, Any


def get_streamlit_callback_handler(parent_container: DeltaGenerator) -> BaseCallbackHandler:
    class StreamHandler(BaseCallbackHandler):

        def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
            self.container = container 
            self.thoughts_placeholder = self.container.container() 
            self.tool_output_placeholder = None 
            self.token_placeholder = self.container.empty() 
            self.text = initial_text

        def on_llm_new_token(self, token: str, **kwargs) -> None:

            self.text += token  
            self.token_placeholder.write(self.text)

        def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
            with self.thoughts_placeholder:
                status_placeholder = st.empty()  
                with status_placeholder.status("执行工具调用...", expanded=True) as s:
                    st.write("工具： ", serialized["name"])  
                    st.write("工具输入: ")
                    st.code(input_str)  
                    st.write("工具输出: ")
                    self.tool_output_placeholder = st.empty()
                    s.update(label="工具调用完成", expanded=False)  

        def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
            if self.tool_output_placeholder:
                self.tool_output_placeholder.code(output.content)   
    
    callback_handler = StreamHandler(parent_container)
    return callback_handler