"""Other structures for Rhodes."""
import attr

from .choice_rules import Not, derive_rule


@attr.s(eq=False, order=False)
class Variable:
    """Represents a JSONPath variable in request/response body."""

    # TODO: Validate the path is a valid JSONPath
    path = attr.ib()

    # TODO: Add __and__ and __or__ behaviors?

    def __lt__(self, other):
        return derive_rule(variable=self.path, operator="<", value=other)

    def __le__(self, other):
        return derive_rule(variable=self.path, operator="<=", value=other)

    def __eq__(self, other):
        return derive_rule(variable=self.path, operator="==", value=other)

    def __ne__(self, other):
        inner_rule = derive_rule(variable=self.path, operator="==", value=other)
        return Not(Rule=inner_rule)

    def __gt__(self, other):
        return derive_rule(variable=self.path, operator=">", value=other)

    def __ge__(self, other):
        return derive_rule(variable=self.path, operator=">=", value=other)
