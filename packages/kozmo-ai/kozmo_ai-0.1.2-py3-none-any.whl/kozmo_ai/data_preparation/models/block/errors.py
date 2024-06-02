from kozmo_ai.errors.base import KozmoBaseException


class NoMultipleDynamicUpstreamBlocks(KozmoBaseException):
    pass


class HasDownstreamDependencies(KozmoBaseException):
    pass
