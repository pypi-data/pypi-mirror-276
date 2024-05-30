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
