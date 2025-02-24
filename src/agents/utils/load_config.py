import json5
from pprint import pp
from typing import Dict
import datetime


def load_config(config_path: str) -> Dict:
    with open(config_path, "r") as f:
        config = json5.load(f)

    print(datetime.datetime.now(), "Loaded config:")
    pp(config)

    return config
