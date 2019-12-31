"""
`AWS Glue <https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html>`_ Task state.
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration

__all__ = ("AwsGlue",)


@attr.s(eq=False)
@service_integration(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS)
class AwsGlue(State):
    """
    :param JobName: The name of the job definition to use.
    :param JobRunId: The ID of a previous JobRun to retry.
    :param Arguments: The job arguments specifically for this run.
    :param AllocatedCapacity: This field is deprecated. Use MaxCapacity instead.
       The number of AWS Glue data processing units (DPUs) to allocate to this JobRun.
    :param Timeout: The JobRun timeout in minutes.
    :param SecurityConfiguration: The name of the SecurityConfiguration structure to be used with this job run.
    :param NotificationProperty: Specifies configuration properties of a job run notification.
    """

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
