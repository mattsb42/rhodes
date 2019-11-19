"""AWS Glue Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html
"""
import attr

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns


@attr.s(eq=False)
@_supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS)
class AwsGlue(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.GLUE

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html

    JobName = attr.ib(default=None)
    JobRunId = attr.ib(default=None)
    Arguments = attr.ib(default=None)
    # TODO: AllocatedCapacity is deprecated; Will SFn's integration change?
    AllocatedCapacity = attr.ib(default=None)
    Timeout = attr.ib(default=None)
    SecurityConfiguration = attr.ib(default=None)
    NotificationProperty = attr.ib(default=None)
