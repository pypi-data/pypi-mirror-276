'''
    Step Json
'''
import json

from api_pipe.api import ApiPipe

def run_step(self: ApiPipe, indent: int) -> object:
    '''
        Run step

        object is an ApiPipe object
        (Due to circular imports)
    '''
    self.log.debug(
        f"Converting from {self.type} to json"
    )

    self.data = json.dumps(
        self.data,
        indent=indent
    )

    self.type = "json"

    self._log_step_to_file(
        "to_json",
        f"to JSON",
        self.data
    )

    return self
