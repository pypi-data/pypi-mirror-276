# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of API Pipe.
#
# API Pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# API Pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with API Pipe. If not, see <http://www.gnu.org/licenses/>.

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
