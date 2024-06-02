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
    API
'''
import httpx
import itertools
from typing import Any
import json
import logging
from pathlib import Path
import importlib

from api_pipe.params import ApiParams
from api_pipe import logger
from api_pipe import directory
from api_pipe.url import Url
from api_pipe.error import InvalidParam
from api_pipe.error import ParamTypeError

MODULE_STEPS_RELATIVE_PATH = Path(__file__).parent / "steps"
LOGS_DIR_NAME_STEPS = "steps"
LOGS_DIR_NAME_APP = "app"
LOGS_STDOUT_FILENAME = "stdout.log"
JSON_INDENT = 2

class ApiPipe:
    '''
        API Pipe
    '''

    def __init__(self,
            url: Url,
            client: httpx.Client | httpx.AsyncClient,
            api_params: ApiParams
        ) -> None:
        '''
            Init

            Params:
                - url: Url to fetch
                - client: client to use for fetching
                - api_params: parameters for the API
        '''
        self.__validate_params(
            url,
            client,
            api_params
        )
        self.__param_routing(
            url,
            client,
            api_params
        )
        self.__import_steps_from_dir(
            MODULE_STEPS_RELATIVE_PATH
        )
        self.__setup_logging()

        self.data : list | dict | str | None  = None
        self.type : str = "Unknown"
        self.curr_step = itertools.count(1)

    def __getattr__(self, name):
        '''
            Map to Step

            Intercepts the call to a method that doesn't exist (presumably a step)
            and redirects it to the corresponding step module. Assumes step
            modules are loaded in the global namespace (i.e. have been imported).

            Raises AttributeError if the step module doesn't exist.
        '''
        def step_function(*args, **kwargs):

            try:
                return globals()[name].run_step(self, *args, **kwargs)
            except KeyError:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{name}'"
                )

        return step_function

    def __import_steps_from_dir(self, steps_dir: Path) -> None:
        '''
            Import Steps from Dir

            Dynamically imports all the steps from the directory
            Path. Assumes the directory contains only steps. Ignores
            anything with '__' in the filename.
        '''
        # gather all step names
        # from the filenames in the /steps
        step_names = [
            file.stem
            for file in steps_dir.iterdir()
            if file.is_file() and file.suffix == ".py" and "__" not in file.stem
        ]

        # import
        for step_name in step_names:
            globals()[step_name] = importlib.import_module(f"api_pipe.steps.{step_name}")

    def __setup_logging(self) -> None:
        '''
            Setup Logging

            Sets up logging for the API
        '''
        self.log_dir_app = self.log_dir / LOGS_DIR_NAME_APP / self.log_unique_name
        self.log_dir_steps = self.log_dir / LOGS_DIR_NAME_STEPS / self.log_unique_name

        # init logs directory
        is_debug_mode = self.log_level == logging.DEBUG
        must_recreate = is_debug_mode
        log_stdout_filepath = self.log_dir_app / LOGS_STDOUT_FILENAME

        directory.remove_dir(
            self.log_dir_app,
            must_recreate
        )
        directory.remove_dir(
            self.log_dir_steps,
            must_recreate
        )
        directory.remove_file(
            self.log_dir_app / LOGS_STDOUT_FILENAME,
            must_recreate
        )

        self.log = logger.stdout(
            self.log_unique_name,
            self.log_level,
            self.log_words_to_highlight,
            log_stdout_filepath if is_debug_mode else None
        )

    def __validate_params(
            self,
            url: Url,
            client: httpx.Client | httpx.AsyncClient,
            api_params: ApiParams
    ) -> None:
        '''
            Validate Params

            Validates the parameters this object receives

            Params:
                - url: Url to fetch
                - client: client to use for fetching
                - api_params: parameters for the API
        '''
        if client is None:
            raise InvalidParam(
                "client",
                "is None"
            )

        if not isinstance(client, httpx.Client) \
            and not isinstance(client, httpx.AsyncClient):
            raise ParamTypeError(
                "client",
                f"{httpx.Client} or {httpx.AsyncClient}",
                client
            )

        if url is None:
            raise InvalidParam(
                "url",
                "is None"
            )

        if not isinstance(url, Url):
            raise ParamTypeError(
                "url",
                Url,
                type(url)
            )

        if not api_params:
            raise InvalidParam(
                "api_params",
                "is None"
            )

        if not isinstance(api_params, ApiParams):
            raise ParamTypeError(
                "api_params",
                ApiParams,
                type(api_params)
            )

        # at this point params are validated
        # but there's a specific use case:
        #  - when using the same params for multiple uses
        #    and params are changed in one use
        api_params.validate()


    def __param_routing(
            self,
            url: Url,
            client: httpx.Client | httpx.AsyncClient,
            api_params: ApiParams
        ) -> None:
        '''
            Param Routing

            Routes param from ApiParams to this object.

            This is handy for:
            - When ApiParams changes we only need to change here.
            - Reduce cognitive load when reading the code.

            Params:
                - url: Url to fetch
                - client: client to use for fetching
                - api_params: parameters for the API
        '''
        self.client : httpx.Client | httpx.AsyncClient = client
        self.url : Url = url

        # API Params
        # Convention is:
        # self.<param_name>_<subparam_name> = api_params.<param_name>['<subparam_name>']

        self.headers: dict[str, Any] = api_params.headers
        self.timeout: tuple[float, float] = api_params.timeout

        self.retries_initial_delay: float = api_params.retries["initial_delay"]
        self.retries_backoff_factor: int = api_params.retries["backoff_factor"]
        self.retries_max_retries: int = api_params.retries["max_retries"]

        self.log_unique_name: str = api_params.logs["unique_name"]
        self.log_dir: Path = api_params.logs["log_dir"]
        self.log_level: int = api_params.logs["level"]
        self.log_words_to_highlight: list[str] = api_params.logs["words_to_highlight"]

    def _log_step_to_file(
            self,
            step_name: str,
            header: str,
            data: Any,
        ) -> None:
        '''
            Log Step To File

            Params:
                - step_name: name of the step
                - header: header for the log
                - data: data to log

            Sample log:

                select keys: ['key', 'value', 'masked']
                -------------------------------------
                            python
                -------------------------------------
                [
                {
                    "key": "Var2",
                    "value": "Value2",
                    "masked": false
                }
                ]
        '''
        if self.log_level > logging.DEBUG:
            return

        log_path = self.log_dir_steps / f"{next(self.curr_step)}_{step_name}.log"

        with open(log_path, "a") as file:
            if header:
                file.write(
                    f"{header}\n"
                )
                file.write(
                    f"-------------------------------------\n"
                    f"              {self.type}            \n"
                    f"-------------------------------------\n"
                )
            if isinstance(data, dict) or isinstance(data, list):
                file.write(
                    json.dumps(
                        data,
                        indent=JSON_INDENT
                    )
                )
            else:
                file.write(str(data))


