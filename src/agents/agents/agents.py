from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate

from . import prompts


def _get_agent(model: BaseChatModel, system_prompt: str) -> Runnable:
    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("placeholder", "{messages}"),
        ]
    )

    return prompt | model


def get_analyzer_agent(model: BaseChatModel) -> Runnable:
    return _get_agent(model, prompts.ANALYZER_SYSTEM_INSTRUCTION)
