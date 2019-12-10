"""AWS Service Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html

All fields that would normally be collected in the ``Parameters`` parameter
are collapsed to the main instantiation level for all ``ServiceIntegration`` classes.
They are internally collected into a ``Parameters`` instance that is assigned to
the ``Parameters`` parameter when these are converted into ``Task`` instances.

The rules for these values are as follows:

* If Step Functions expects a single value,
   the value can be a string, a :class:`JsonPath`,
   or a :class:`troposphere.AWSHelperFn`.
* If Step Functions can accept a complex value,
   the value can be a :class:`JsonPath`,
   :class:`Parameters`, or a :class:`troposphere.AWSHelperFn`.
* If the value represents an AWS resource,
   such as a Lambda Function or Step Functions State Machine,
   the value can be the appropriate Troposphere type.

Any of these values can also be an :class:`Enum`.
If you choose to use an :class:`Enum`
and the instance value is NOT one of the above appropriate types,
the serialization will fail.

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
