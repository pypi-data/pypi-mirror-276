from kozmo_ai.errors.base import KozmoBaseException
from typing import Dict


class DoesNotExistError(KozmoBaseException):
    pass


class ValidationError(KozmoBaseException):
    def __init__(self, error: str, metadata: Dict):
        self.error = error
        self.metadata = metadata

    def to_dict(self):
        return dict(
            error=self.error,
            metadata=self.metadata,
        )
