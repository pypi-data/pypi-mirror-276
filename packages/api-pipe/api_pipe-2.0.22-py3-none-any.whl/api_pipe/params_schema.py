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
