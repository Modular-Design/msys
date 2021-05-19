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


