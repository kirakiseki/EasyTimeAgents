import os

from .load_config import load_config

CONFIG = load_config("config.json5")
os.environ["ZHIPUAI_API_KEY"] = CONFIG["models"]["zhipuai"]["api_key"]
