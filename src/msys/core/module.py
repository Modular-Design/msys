from .unit import UniqueUnit
from .serializer import ConnectableList
from .unit import Unit

class Module(UniqueUnit):
    def __init__(self, inputs=[], outputs=[], options=[], sub_modules=[], inputs_generator=None, outputs_generator=None):
        self.inputs = ConnectableList(inputs, inputs_generator)
        self.outputs = ConnectableList(outputs, outputs_generator)
        self.options = options
        self.modules = []
        for module in sub_modules:
            self.add_module(module)
        super().__init__()

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

    def get_options(self):
        return self.options

    def get_childs(self) -> []:
        return self.inputs[:] + self.outputs[:] + self.modules

    def add_module(self, module: Unit):
        module.parent = self
        self.modules.append(module)

    def to_dict(self) -> dict:
        res = super().to_dict()
        options = []
        for o in self.options:
            options.append(o.to_dict())
        res["options"] = options

        res["inputs"] = self.inputs.to_dict()

        res["outputs"] = self.outputs.to_dict()
        return res

    def from_dict(self, json: dict) -> bool:
        found = super().from_dict(json)

        def _from_dict(key, lists, changeable=False):
            connectables = json[key]
            for new_c in connectables:
                found = False
                if not "id" in new_c:
                    break
                for old_c in lists:
                    if new_c["id"] == old_c.id:
                        old_c.from_dict(new_c)
                        break

        if "options" in json.keys():
            _from_dict("options", self.options)
            found = True

        if "inputs" in json.keys():
            self.inputs.from_dict(json["inputs"])
            found = True

        if "outputs" in json.keys():
            self.outputs.from_dict(json["outputs"])
            found = True

        return found

    def process(self) -> None:
        """
        Overide this methode!
        :return:
        """
        pass

    def update(self) -> bool:
        changed = self.inputs.update()

        if changed:
            self.process()

        changed = self.outputs.update()
        return changed
