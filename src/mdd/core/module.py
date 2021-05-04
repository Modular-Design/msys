from .unit import UniqueUnit


class Module(UniqueUnit):
    def __init__(self, inputs=[], outputs=[], options=[]):
        self.inputs = inputs
        self.outputs = outputs
        self.options = options
        super().__init__()

    def get_childs(self) -> []:
        return self.inputs + self.outputs

    def to_dict(self) -> dict:
        res = super().to_dict()
        options = []
        for o in self.options:
            options.append(o.to_dict())
        res["options"] = options

        inputs = []
        for i in self.inputs:
            inputs.append(i.to_dict())
        res["inputs"] = inputs

        outputs = []
        for o in self.outputs:
            outputs.append(o.to_dict())
        res["outputs"] = outputs
        return res

    def from_dict(self, json: dict) -> bool:
        if not super().from_dict(json):
            return False

        def _from_dict(key, lists):
            connectables = json[key]
            for new_c in connectables:
                if not "id" in new_c:
                    break
                for old_c in lists:
                    if new_c["id"] == old_c.id:
                        old_c.from_dict(new_c)
                        break

        if "options" in json.keys():
            _from_dict("options", self.options)

        if "inputs" in json.keys():
            _from_dict("inputs", self.inputs)

        if "outputs" in json.keys():
            _from_dict("outputs", self.outputs)

    def process(self) -> None:
        """
        Overide this methode!
        :return:
        """
        pass

    def update(self) -> bool:
        changed = False
        for ins in self.inputs:
            if ins.update():
                changed = True

        if changed:
            self.process()

        for outs in self.outputs:
            if outs.update():
                changed = True
        return changed


