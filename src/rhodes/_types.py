from enum import Enum
from typing import Any, Optional, TypeVar, Union

import jsonpath_rw
from troposphere import AWSHelperFn, awslambda, stepfunctions

from rhodes.choice_rules import ChoiceRule
from rhodes.identifiers import ServiceArn
from rhodes.states import State, StateMachine
from rhodes.structures import JsonPath, Parameters

StateMirror = TypeVar("StateMirror", bound=State)
StateMachineMirror = TypeVar("StateMachineMirror", bound=StateMachine)
ChoiceRuleMirror = TypeVar("ChoiceRuleMirror", bound=ChoiceRule)

# path inputs
PATH_INPUT = Union[str, Enum, jsonpath_rw.JSONPath, JsonPath]

TITLE = str
COMMENT = Optional[str]
NEXT = Optional[str]
END = Optional[bool]
INPUT_PATH = JsonPath
OUTPUT_PATH = JsonPath
RESULT_PATH = JsonPath
PARAMETERS = Optional[Parameters]
CATCH = Optional[Any]
RETRY = Optional[Any]
TIMEOUT_SECONDS = Optional[int]
HEARTBEAT_SECONDS = Optional[int]

# resource types for the type stub to use
TASK_RESOURCE = Union[ServiceArn, str, awslambda.Function, stepfunctions.Activity, AWSHelperFn]

SERVICE_INTEGRATION_SIMPLE_VALUE = Union[str, JsonPath, Enum, AWSHelperFn]
SERVICE_INTEGRATION_COMPLEX_VALUE = Union[JsonPath, Enum, AWSHelperFn, Parameters]
AWS_LAMBDA_FUNCTION = Union[str, JsonPath, Enum, AWSHelperFn, awslambda.Function]
