from kozmo_ai.errors.base import KozmoBaseException


class FileExistsError(KozmoBaseException):
    pass


class FileNotInProjectError(KozmoBaseException):
    pass


class FileWriteError(KozmoBaseException):
    pass


class SerializationError(KozmoBaseException):
    pass


class PipelineZipTooLargeError(KozmoBaseException):
    pass


class InvalidPipelineZipError(KozmoBaseException):
    pass
