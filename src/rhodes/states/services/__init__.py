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
