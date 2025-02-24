from langchain_zhipu import ChatZhipuAI
from langchain_core.language_models import BaseChatModel
from utils import CONFIG


def _get_model(model_name: str) -> BaseChatModel:
    match CONFIG["provider"]:
        case "zhipuai":
            model = ChatZhipuAI(
                model=CONFIG["models"]["zhipuai"][model_name],
                temperature=CONFIG["models"]["zhipuai"]["temperature"],
                streaming=True,
            )
        case _:
            raise ValueError("Invalid provider")

    return model


def get_lite_llm() -> BaseChatModel:
    return _get_model("llm_model_lite")


def get_plus_llm() -> BaseChatModel:
    return _get_model("llm_model_plus")


def get_vlm() -> BaseChatModel:
    return _get_model("vlm_model")
