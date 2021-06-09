import weakref
from .interfaces import SerializerInterface
from .connectable import Connectable

class Connection(SerializerInterface):
    def __init__(self, parent = None, output = None, input = None):
        self.parent = parent
        self.out_ref = weakref.ref(output)
        self.in_ref = weakref.ref(input)
        self.meta = []


    def to_dict(self) -> dict:
        input = self.in_ref()
        output = self.out_ref()

        if input is None or output is None:
            del self
            return None
        return {json.dumps(output.identifier()): {input.identifier(): self.meta}}


    def from_dict(self, json: dict) -> bool:
        if self.out_ref() is None:
            self.out_ref = weakref.ref(parent.find(json.keys()[0]))
        elif json.dumps(self.out_ref().identifier()) == json.keys()[0]:
            self.out_ref = weakref.ref(parent.find(json.keys()[0]))

        json = json.get(json.dumps(self.out_ref().identifier()))
        if not json:
            return False
        if self.in_ref() is None:
            self.in_ref = weakref.ref(parent.find(json.keys()[0]))
        elif json.dumps(self.in_ref().identifier()) == json.keys()[0]:
            self.in_ref = weakref.ref(parent.find(json.keys()[0]))

        self.meta = json.get(json.dumps(self.in_ref().identifier()))
        return True