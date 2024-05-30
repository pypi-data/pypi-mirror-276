'''
    Step Map
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
        f"Mapping {self.type}. \nMapping Function:   \n{function_code}"
    )

    if isinstance(self.data, dict):
        self.data = {
            k: function(v) for k, v in self.data.items()
        }
    elif isinstance(self.data, list):
        self.data = list(map(function, self.data))
    else:
        raise OperationInvalidType(
            "map",
            self.type
        )

    self.type = self.type

    try:
        self._log_step_to_file(
            "map",
            f"map function:\n   {function_code}",
            self.data
        )
    except TypeError as e:
        self.log.warning(
            f"Cannot log map function: {e}. Logging data only."
        )
        self._log_step_to_file(
            "map",
            f"map function: OMMITED (could not log function)",
            self.data
        )

    return self
