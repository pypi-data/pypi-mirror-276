from kozmo_ai.errors.base import KozmoBaseException


class WorkspaceExistsError(KozmoBaseException):
    pass


class ConfigurationError(KozmoBaseException):
    pass
