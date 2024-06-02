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
    Step Fetch Async
'''
import json
import asyncio
from api_pipe.api import ApiPipe

from api_pipe.error import FetchMaxAttempts
from httpx import Response

async def run_step(self: ApiPipe) -> object:
    '''
        Run step

        object is an ApiPipe object
        (Due to circular imports)
    '''
    self.log.info(
        f"Async Fetching from {self.url}"
    )

    for attempt in range(self.retries_max_retries):
        self.log.debug(
            f"Attempt: {attempt + 1} of {self.retries_max_retries}"
        )
        try:
            response : Response = await self.client.get(
                str(self.url),
                timeout=self.timeout,
                headers=self.headers
            )
            response.raise_for_status()

            break
        except Exception as e:
            if attempt == self.retries_max_retries - 1:
                self.log.error(
                    f"{self.log_unique_name}. Attempted max times {self.retries_max_retries}"
                )
                raise FetchMaxAttempts(
                    self.url,
                    self.retries_max_retries
                ) from e
            sleeping_time = self.retries_initial_delay * (self.retries_backoff_factor ** attempt)
            self.log.warning(
                f"{self.log_unique_name}. "
                f"\nRetrying fetch for URL {self.url}. Attempt: {attempt + 1} of {self.retries_max_retries}."
                f"\nError: {e}"
                f"\nSleeping for {sleeping_time} seconds"
            )

            for handler in self.log.handlers:
                handler.flush()

            await asyncio.sleep(
                sleeping_time
            )


    self.data = response.text

    self.type = "text"

    self._log_step_to_file(
        "fetch_async",
        f"GET {self.url}\n{json.dumps(self.headers)}",
        self.data
    )

    return self
