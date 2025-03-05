from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage

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


def get_evaluator_agent(
    model: BaseChatModel,
) -> RunnableSerializable[dict, BaseMessage]:
    prompt = ChatPromptTemplate(
        [
            ("placeholder", "{messages}"),
            ("system", prompts.EVALUATOR_SYSTEM_INSTRUCTION),
        ]
    )

    return prompt | model


def get_worker_agent(model: BaseChatModel) -> RunnableSerializable[dict, BaseMessage]:
    model_with_stop = model.bind(stop=["\nObservation"])

    prompt = ChatPromptTemplate(
        [
            ("placeholder", "{messages}"),
            ("system", prompts.WORKER_SYSTEM_INSTRUCTION),
        ]
    )

    return prompt | model_with_stop


def get_visualizer_agent(
    model: BaseChatModel,
) -> RunnableSerializable[dict, BaseMessage]:
    return _get_agent(model, prompts.VISUALIZER_SYSTEM_INSTRUCTION)
