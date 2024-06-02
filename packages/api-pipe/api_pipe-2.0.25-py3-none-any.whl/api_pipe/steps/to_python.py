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
    Step Fetch
'''
import json

from api_pipe.api import ApiPipe

def run_step(self: ApiPipe) -> object:
    '''
        Run step

        object is an ApiPipe object
        (Due to circular imports)
    '''
    self.log.debug(
        f"Converting from {self.type} to python object"
    )

    try:
        self.data = json.loads(self.data)
    except json.JSONDecodeError:
        self.log.warning(
            f"fecthed data is not in JSON format."
            f"\nHere's a small sample data: {self.data[:100]}..."
            "\nCarrying on, setting to []"
        )
        self.data = []

    self.type = "python"

    self._log_step_to_file(
        "to_python",
        f"to python",
        self.data
    )

    return self
