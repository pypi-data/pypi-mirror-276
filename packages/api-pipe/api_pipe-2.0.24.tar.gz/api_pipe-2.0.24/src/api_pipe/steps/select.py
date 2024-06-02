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
    Step Select
'''
from api_pipe.api import ApiPipe
from api_pipe.error import OperationInvalidType

def run_step(self: ApiPipe, keys: list[str]) -> object:
    '''
        Run step

        object is an ApiPipe object
        (Due to circular imports)
    '''
    self.log.debug(
        f"Selecting keys from {self.type}.\nKeys: {keys}"
    )

    if isinstance(self.data, dict):
        self.data = {
            key: self.data[key]
            for key in keys if key in self.data
        }
    elif isinstance(self.data, list):
        self.data = [
            {k: v for k, v in d.items() if k in keys} for d in self.data
        ]
    else:
        raise OperationInvalidType(
            "select",
            self.type
        )

    self.type = self.type   #just for consistency

    self._log_step_to_file(
        "select",
        f"select keys: {keys}",
        self.data
    )

    return self
