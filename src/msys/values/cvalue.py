from pymsys.values import Value
from typing import Optional


class ConnectedValue(Value):
    def __init__(self, default_value: Optional[dict] = None):
        super().__init__(default_value)

    def is_allowed(self, config: dict) -> bool:
        child_list = self.connectable.get_parent()
        if child_list is None:
            raise ValueError

        for outgoing in self.get_inputs():  # TODO: Think about a better solution of type validation
            if not outgoing.is_data_valid(config):
                return False
        return True

