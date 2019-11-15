"""Exceptions for use in Rhodes."""


class RhodesError(Exception):
    pass


class IncompleteDefinitionError(RhodesError):
    pass


class InvalidDefinitionError(RhodesError):
    pass
