import streamlit as st
import inspect
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from langchain_core.callbacks.base import BaseCallbackHandler
from typing import Dict, Any, TypeVar, Callable


def tool_call_inputs_renderer(args: Dict[str, Any]) -> str:
    return "\n".join(f"{k}: {v}" for k, v in args.items())


def get_streamlit_callback_handler(
    parent_container: DeltaGenerator,
) -> BaseCallbackHandler:
    class StreamHandler(BaseCallbackHandler):

        def __init__(
            self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""
        ):
            self.container = container
            self.content_container = self.container.empty()
            self.tool_container = None
            self.tool_status = None
            self.tool_output_placeholder = None
            self.text = initial_text

        def on_llm_new_token(self, token: str, **kwargs) -> None:
            self.text += token
            self.content_container.write(self.text)

        def on_tool_start(
            self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
        ) -> None:
            self.tool_container = self.container.empty()
            self.tool_status = self.tool_container.status(
                "执行工具调用...", expanded=True
            )

            self.content_container = self.container.empty()
            self.text = ""

            with self.tool_status as s:
                inputs = kwargs.get("inputs", {})
                st.write("工具： ", serialized["name"])
                st.write("工具输入: ")
                st.code(tool_call_inputs_renderer(inputs))
                st.write("工具输出: ")
                self.tool_output_placeholder = st.empty()

        def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
            with self.tool_status as s:
                s.update(label="工具调用完成", expanded=True)

                if self.tool_output_placeholder:
                    self.tool_output_placeholder.code(output.content)

    fn_return_type = TypeVar("fn_return_type")

    def add_streamlit_context(
        fn: Callable[..., fn_return_type]
    ) -> Callable[..., fn_return_type]:
        ctx = get_script_run_ctx()

        def wrapper(*args, **kwargs) -> fn_return_type:
            add_script_run_ctx(ctx=ctx)
            return fn(*args, **kwargs)

        return wrapper

    callback_handler = StreamHandler(parent_container)

    for method_name, method_func in inspect.getmembers(
        callback_handler, predicate=inspect.ismethod
    ):
        if method_name.startswith("on_"):
            setattr(callback_handler, method_name, add_streamlit_context(method_func))

    return callback_handler
