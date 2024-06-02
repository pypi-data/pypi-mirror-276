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
    Params
'''
from dataclasses import dataclass
from typing import Any
from dataclasses import fields
from dataclasses import field

from api_pipe.params_schema import SCHEMA
from api_pipe.error import MissingParam
from api_pipe.error import ParamTypeError
from api_pipe.error import InvalidParam
from api_pipe.error import UnrecognizedParam

DEFAULT_TIMEOUT = (5.0, 5.0)
DEFAULT_RETRIES = {
    "initial_delay": 0.5,
    "backoff_factor": 3,
    "max_retries": 3,
}

@dataclass
class ApiParams:
    '''
        API Params
    '''
    headers : dict = field(default_factory=dict)
    timeout : tuple[float, float] = field(default_factory=lambda: DEFAULT_TIMEOUT)
    retries : dict[str, Any] = field(default_factory=lambda: DEFAULT_RETRIES)
    logs : dict = field(default_factory=dict)

    def __post_init__(self):
        '''
            Post init
        '''
        self.validate()

    def __str__(self) -> str:
        '''
            String representation
        '''
        return f"ApiParams(headers={self.headers}, timeout={self.timeout}, retries={self.retries}, logs={self.logs})"

    def validate(self) -> None:
        '''
            Validates params against parameters schemas.
        '''
        for field in fields(self):

            try:
                param_name = field.name
                param_value = getattr(self, param_name)
            except AttributeError as e:
                raise MissingParam(
                    param_name
                ) from e

            try:
                self.__validate_param(
                    param_name,
                    param_value,
                    SCHEMA[param_name]
                )
            except KeyError as e:
                raise UnrecognizedParam(
                    param_name
                ) from e


    def __validate_param(
            self,
            param_name: str,
            param_value: Any,
            param_schema: dict[str, Any]
        ) -> None:
        '''
            Validate single parameter against a parameter schema entry
        '''
        if not isinstance(
            param_value,
            param_schema["type"]
        ):
            raise ParamTypeError(
                param_name,
                param_schema["type"],
                type(param_value)
            )

        if "tuple_items" in param_schema:

            if len(param_value) < param_schema["minItems"] \
                or len(param_value) > param_schema["maxItems"]:

                raise InvalidParam(
                    param_name,
                    f"expected between {param_schema["minItems"]} "
                    f"and {param_schema["maxItems"]} items. Received {len(param_value)}."
                )

            for i, item in enumerate(param_value):
                if not isinstance(item, param_schema["tuple_items"]["type"]):
                    raise ParamTypeError(
                        f"{param_name}[{i}]",
                        param_schema["tuple_items"]["type"],
                        type(item)
                    )
        if "properties" in param_schema:
            for property_name in param_schema["properties"]:
                try:
                    self.__validate_param(
                        property_name,
                        param_value[property_name],
                        param_schema["properties"][property_name]
                    )
                except KeyError as e:
                    raise MissingParam(
                        f"{param_name}.{property_name}"
                    ) from e



