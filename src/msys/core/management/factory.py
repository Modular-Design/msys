
class Factory:
    def __init__(self):
        self.instances= dict()

    def create_instance(self, name: str):
        pass

    def change_instance(self, name: str, change: dict):
        pass

    def save_instance(self, name: str):
        pass

    def close_instance(self, name: str):
        pass
