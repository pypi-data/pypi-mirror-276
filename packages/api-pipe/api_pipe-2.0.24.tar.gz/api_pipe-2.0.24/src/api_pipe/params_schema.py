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
    Params schema for param validation in api_pipe
'''
from pathlib import Path

SCHEMA: dict[str, dict] = {
    "headers": {
        "type": dict
    },
    "timeout": {
        "type": tuple,
        "tuple_items": {
            "type": float
        },
        "minItems": 2,
        "maxItems": 2
    },
    "retries": {
        "type": dict,
        "properties": {
            "initial_delay": {
                "type": float
            },
            "backoff_factor": {
                "type": int
            },
            "max_retries": {
                "type": int
            }
        }
    },
    "logs": {
        "type": dict,
        "properties": {
            "unique_name": {
                "type": str
            },
            "log_dir": {
                "type": Path
            },
            "level": {
                "type": int
            },
            "words_to_highlight": {
                "type": list,
                "items": {
                    "type": str
                }
            }
        }
    }
}
