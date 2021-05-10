
class ConnectableInterface:
    def get_value(self) -> []:
        pass

    def set_value(self, value) -> bool:
        pass

    def is_optimized(self) -> bool:
        pass

    def set_optimized(self, optimized: bool) -> bool:
        pass

    def is_changed(self) -> bool:
        pass

    def is_connected(self) -> bool:
        pass

    def connect(self, connectable, both=True) -> bool:
        """Try to connect to connectable."""
        pass

    def disconnect(self, connectable=None, both=True) -> bool:
        """Try to disconnect to connectable."""
        pass

    def __del__(self):
        self.disconnect()
