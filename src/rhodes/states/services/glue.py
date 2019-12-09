"""AWS Glue Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.util import supports_patterns


@attr.s(eq=False)
@supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS)
class AwsGlue(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.GLUE

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html

    JobName = RHODES_ATTRIB()
    JobRunId = RHODES_ATTRIB()
    Arguments = RHODES_ATTRIB()
    # TODO: AllocatedCapacity is deprecated; Will SFn's integration change?
    AllocatedCapacity = RHODES_ATTRIB()
    Timeout = RHODES_ATTRIB()
    SecurityConfiguration = RHODES_ATTRIB()
    NotificationProperty = RHODES_ATTRIB()
