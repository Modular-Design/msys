from .unit import UniqueUnit


class Module(UniqueUnit):
    def __init__(self, inputs=[], outputs=[], options=[]):
        self.inputs = inputs
        self.outputs = outputs
        self.options = options
        super().__init__()

    def getchilds(self) -> []:
        return self.inputs + self.outputs

    def toDict(self) -> dict:
        res = super().toDict()
        options = []
        for o in self.options:
            options.append(o.toDict())
        res["options"] = options
        return res


