
def includes(array: [], elements: []) -> bool:
    for e in elements:
        if not e in array:
            return False
    return True


class SerializerInterface:
    def fromDict(self, json: dict) -> bool:
        """Load class from dictionary."""
        pass

    def toDict(self) -> dict:
        """Gerenate dict from class."""
        pass
