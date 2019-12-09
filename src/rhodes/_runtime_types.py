from typing import Any, Tuple

from rhodes.identifiers import ServiceArn

try:
    from troposphere import awslambda, stepfunctions, Ref, GetAtt

    TROPOSPHERE = True
except ImportError:
    TROPOSPHERE = False

# resource types for the validator to use
TASK_RESOURCE_TYPES: Tuple = (ServiceArn, str)
if TROPOSPHERE:
    TASK_RESOURCE_TYPES += (awslambda.Function, stepfunctions.Activity, Ref, GetAtt)
