from dataclasses import dataclass
from kozmo_ai.shared.config import BaseConfig


@dataclass
class Config(BaseConfig):
    """
    https://docs.metaplane.dev/reference/getting-started
    """

    api_token: str
