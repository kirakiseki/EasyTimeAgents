from gradio.server_messages import BaseMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable
from langchain_core.prompts import ChatPromptTemplate

from . import prompts


def _get_agent(
    model: BaseChatModel, system_prompt: str
) -> RunnableSerializable[dict, BaseMessage]:
    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("placeholder", "{messages}"),
        ]
    )

    return prompt | model


def get_greeting_agent(model: BaseChatModel) -> RunnableSerializable[dict, BaseMessage]:
    return _get_agent(model, prompts.GREETING_SYSTEM_INSTRUCTION)


def get_checker_agent(model: BaseChatModel) -> RunnableSerializable[dict, BaseMessage]:
    return _get_agent(model, prompts.CHECKER_SYSTEM_INSTRUCTION)


def get_decomposer_agent(
    model: BaseChatModel,
) -> RunnableSerializable[dict, BaseMessage]:
    return _get_agent(model, prompts.DECOMPOSER_SYSTEM_INSTRUCTION)
