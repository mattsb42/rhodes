"""AWS Service Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html
"""
from typing import Dict

import attr

from rhodes._util import require_field
from rhodes.states import State, Task
from rhodes.states._parameters import task_type
from rhodes.structures import Parameters

__all__ = ("ServiceIntegration",)


@attr.s(eq=False)
@task_type
class ServiceIntegration(State):
    _resource_name = NotImplemented

    def to_dict(self) -> Dict:
        for required in self._required_fields:
            require_field(instance=self, required_value=required)

        task = self._build_task()
        return task.to_dict()

    def _build_task(self) -> Task:
        task_fields = [field.name for field in attr.fields(Task)]
        field_name_blacklist = ("Pattern", "Parameters")
        resource_name = self._resource_name.value + self.Pattern.value

        task_kwargs = {}
        parameters_kwargs = {}

        for field in attr.fields(type(self)):
            if field.name in field_name_blacklist or field.name.startswith("_"):
                continue

            value = getattr(self, field.name)
            if value is None:
                continue

            if field.name in task_fields:
                task_kwargs[field.name] = value
            else:
                parameters_kwargs[field.name] = value

        params = Parameters(**parameters_kwargs)
        return Task(Parameters=params, Resource=resource_name, **task_kwargs)
