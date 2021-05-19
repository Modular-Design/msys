def includes(array: [], elements: []) -> bool:
    for e in elements:
        if not e in array:
            return False
    return True


class SerializerInterface:
    def from_dict(self, json: dict) -> bool:
        """Load class from dictionary."""
        pass

    def to_dict(self) -> dict:
        """Gerenate dict from class."""
        pass

class ConnectableInterface:
    def get_value(self) -> []:
        pass

    def set_value(self, value) -> bool:
        pass

    def get_ingoing(self):
        pass

    def get_outgoing(self) -> []:
        pass

    def get_type(self):
        pass

    def connect_ingoing(self, output) -> bool:
        pass

    def connect_outgoing(self, input) -> bool:
        pass

    def disconnect_ingoing(self) -> bool:
        pass

    def disconnect_outgoing(self) -> bool:
        pass

    def is_changed(self) -> bool:
        pass

    def update(self) -> bool:
        return True

