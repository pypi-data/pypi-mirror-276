'''
    Step Fetch
'''
from api_pipe.api import ApiPipe
from api_pipe.error import OperationInvalidType

def run_step(self: ApiPipe, key: str) -> object:
    '''
        Run step

        object is an ApiPipe object
        (Due to circular imports)
    '''
    self.log.debug(
        f"Selecting key {key} from {self.type}"
    )

    if isinstance(self.data, dict):
        self.data = self.data[key]
    else:
        raise OperationInvalidType(
            "key",
            self.type
        )

    self.type = type(self.data)

    self._log_step_to_file(
        "key",
        f"select key: {key}",
        self.data
    )

    return self
