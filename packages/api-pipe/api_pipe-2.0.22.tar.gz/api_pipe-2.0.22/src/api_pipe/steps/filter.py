'''
    Step Filter
'''
import inspect
from typing import Callable

from api_pipe.api import ApiPipe
from api_pipe.error import OperationInvalidType

def run_step(self: ApiPipe, function: Callable) -> object:
    '''
        Run step

        object is an ApiPipe object
        (Due to circular imports)
    '''
    function_code = inspect.getsource(function).strip()

    self.log.debug(
        f"Filtering {self.type}. \nFilter Function:   \n{function_code}"
    )

    if isinstance(self.data, dict):
        self.data = {
            key: self.data[key]
            for key in self.data if function(key)
        }
    elif isinstance(self.data, list):
        self.data = [
            d for d in self.data if function(d)
        ]
    else:
        raise OperationInvalidType(
            "filter",
            self.type
        )

    self.type = self.type

    self._log_step_to_file(
        "filter",
        f"filter function:\n   {function_code}",
        self.data
    )

    return self
