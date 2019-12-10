from enum import Enum
from typing import Tuple

from rhodes.identifiers import ServiceArn
from rhodes.structures import JsonPath, Parameters

try:
    from troposphere import awslambda, stepfunctions, Ref, GetAtt, AWSHelperFn

    TROPOSPHERE = True
except ImportError:
    TROPOSPHERE = False

# resource types for the validator to use
TASK_RESOURCE_TYPES: Tuple = (ServiceArn, str, Enum)
SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES: Tuple = (str, JsonPath, Enum)
SERVICE_INTEGRATION_COMPLEX_VALUE_TYPES: Tuple = (JsonPath, Parameters, Enum)
AWS_LAMBDA_FUNCTION_TYPES: Tuple = SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES[:]
if TROPOSPHERE:
    TASK_RESOURCE_TYPES += (awslambda.Function, stepfunctions.Activity, AWSHelperFn)
    SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES += (AWSHelperFn,)
    SERVICE_INTEGRATION_COMPLEX_VALUE_TYPES += (AWSHelperFn,)
    AWS_LAMBDA_FUNCTION_TYPES += (awslambda.Function,)
