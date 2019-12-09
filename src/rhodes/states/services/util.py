from typing import Callable, TypeVar

from attr.validators import in_

from rhodes._util import RHODES_ATTRIB
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration

__all__ = ("supports_patterns",)


ServiceIntegrationMirror = TypeVar("ServiceIntegrationMirror", bound=ServiceIntegration)


def supports_patterns(*options: IntegrationPattern) -> Callable[[ServiceIntegrationMirror], ServiceIntegrationMirror]:
    def _decorate(cls: ServiceIntegrationMirror) -> ServiceIntegrationMirror:
        cls.Pattern = RHODES_ATTRIB(default=options[0], validator=in_(options))

        return cls

    return _decorate
