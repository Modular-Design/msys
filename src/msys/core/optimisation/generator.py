from src.msys.core.serializer import SerializerInterface


class Generator(SerializerInterface):
    def generate(self) -> None:
        pass


class Limiter(Generator):
    def __init__(self):
        self.min = []
        self.max = []
        self.step = []
        self.rule = ""
        self.elements = []
