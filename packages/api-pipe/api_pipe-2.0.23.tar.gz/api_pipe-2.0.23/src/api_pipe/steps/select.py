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
