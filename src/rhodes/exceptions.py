"""Exceptions for use in Rhodes."""


class RhodesError(Exception):
    """Common base for all Rhodes exceptions."""


class IncompleteDefinitionError(RhodesError):
    """Raise when an incomplete state machine definition is found."""


class InvalidDefinitionError(RhodesError):
    """Raised when an invalid state machine definition is found."""
