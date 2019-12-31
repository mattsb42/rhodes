from typing import Callable, Dict, TypeVar

import attr
from attr.validators import in_

from rhodes._types import StateMirror
from rhodes._util import RHODES_ATTRIB, docstring_with_param, require_field
from rhodes.identifiers import IntegrationPattern
from rhodes.states import Task
from rhodes.states._parameters import task_type
from rhodes.structures import Parameters

__all__ = ("service_integration",)


def service_integration(*options: IntegrationPattern) -> Callable[[StateMirror], StateMirror]:
    def _decorate(cls: StateMirror) -> StateMirror:
        cls = task_type(cls)

        cls.Pattern = RHODES_ATTRIB(default=options[0], validator=in_(options))
        cls.__doc__ = docstring_with_param(
            cls, "Pattern", IntegrationPattern, description="Step Functions integration pattern", default=options[0]
        )

        def to_dict(instance) -> Dict:
            """Serialize state as a dictionary."""
            for required in instance._required_fields:
                require_field(instance=instance, required_value=required)

            task = instance._build_task()
            return task.to_dict()

        cls.to_dict = to_dict

        def _build_task(instance) -> Task:
            task_fields = [field.name for field in attr.fields(Task)]
            field_name_blacklist = ("Pattern", "Parameters")
            resource_name = instance._resource_name.value + instance.Pattern.value

            task_kwargs = {}
            parameters_kwargs = {}

            for field in attr.fields(type(instance)):
                if field.name in field_name_blacklist or field.name.startswith("_"):
                    continue

                value = getattr(instance, field.name)
                if value is None:
                    continue

                if field.name in task_fields:
                    task_kwargs[field.name] = value
                else:
                    parameters_kwargs[field.name] = value

            params = Parameters(**parameters_kwargs)
            return Task(Parameters=params, Resource=resource_name, **task_kwargs)

        cls._build_task = _build_task

        return cls

    return _decorate
