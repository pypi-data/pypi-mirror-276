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
