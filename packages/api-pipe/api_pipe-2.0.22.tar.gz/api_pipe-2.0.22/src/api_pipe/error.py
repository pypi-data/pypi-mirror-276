'''
    Error
'''
from typing import Any

from api_pipe.url import Url

class MissingParam(Exception):
    '''
        MissingParam.
    '''
    def __init__(self, param_name: str) -> None:
        super().__init__(
            "Missing param: " + param_name
        )

class UnrecognizedParam(Exception):
    '''
        UnrecognizedParam
    '''
    def __init__(self, param_name: str) -> None:
        super().__init__(
            "Unrecognized param: " + param_name
        )

class ParamTypeError(TypeError):
    '''
        ParamTypeError
    '''
    def __init__(self, param_name: str, expected_type: Any, actual_type: Any) -> None:
        super().__init__(
            f"Param '{param_name}' must be of type '{expected_type}' "
            f"but it's of type '{actual_type}'"
        )

class InvalidParam(Exception):
    '''
        InvalidParam
    '''
    def __init__(self, param_name: str, reason: str) -> None:
        super().__init__(
            f"Invalid param: {param_name}. Reason: {reason}"
        )

class OperationInvalidType(Exception):
    '''
        StepError
    '''
    def __init__(self, operation_name: str, data_type: str) -> None:
        super().__init__(
            f"Operation '{operation_name}' not supported for data type '{data_type}'"
        )

class FetchMaxAttempts(Exception):
    '''
        MaxAttempts
    '''
    def __init__(self, url: Url, max_attempts: int) -> None:
        super().__init__(
            f"Attempted max number of attempts ({max_attempts}) "
            f"at fetching data from URL: {str(url)}"
        )
