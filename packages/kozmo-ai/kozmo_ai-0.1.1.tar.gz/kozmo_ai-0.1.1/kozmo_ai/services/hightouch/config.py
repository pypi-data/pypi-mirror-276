from dataclasses import dataclass
from kozmo_ai.shared.config import BaseConfig


@dataclass
class HightouchConfig(BaseConfig):
    api_key: str
