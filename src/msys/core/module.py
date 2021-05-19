from .unit import UniqueUnit
from .interfaces import ConnectableInterface
from .serializer_lists import ConnectableList
from .connectable import ConnectableFlag, Connectable
from .unit import Unit

class Module(UniqueUnit):
    def __init__(self, inputs=[], outputs=[], options=[], sub_modules=[], inputs_generator=None, outputs_generator=None):
        self.inputs = ConnectableList(self, inputs, ConnectableFlag.INPUT)
        self.outputs = ConnectableList(self, outputs, ConnectableFlag.OUTPUT)
        self.options = options
        self.modules = []
        for module in sub_modules:
            self.add_module(module)
        super().__init__()

    def get_inputs(self):
        return list(self.inputs)

    def get_outputs(self):
        return list(self.outputs)

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

    def is_tree(self)->bool:
        """


        """

        found_modules = []
        for i in range(len(self.modules)):
            run = []
            def move_from(module) -> bool:
                run.append(module)
                outputs = module.get_outputs()
                for out in outputs:
                    parent = out.parent
                    # prevent from going outside
                    if not parent in self.modules:
                        continue
                    # preventing double findings
                    if parent in run:
                        continue
                    # if circle
                    if parent is self.modules[i]:
                        return False
                    if not move_from(parent):
                        return False
                return True

            if not move_from(self.modules[i]):
                return False
        return True

    def is_connection_allowed(self)->bool:
        """

        Oberride this function
        Returns:

        """
        return True

    def connect(self, obj0, obj1) -> bool:
        if not (issubclass(obj0.__class__, ConnectableInterface.__class__) and issubclass(obj0.__class__, ConnectableInterface.__class__)):
            return False

        id0 = obj0.identifier()
        id1 = obj1.identifier()
        len_diff = len(id1)-len(id0)
        if abs(len_diff) > 1:
            return False

        if len_diff < 0:
            obj1, obj0 = obj0, obj1
            id0 = obj0.identifier()
            id1 = obj1.identifier()
            len_diff = abs(len_diff)
        # obj0 is higher or level with obj1

        # number of same levels
        same_till = 0
        for i in range(len(id0)):
            if id0[i] != id1[i]:
                break
            ++same_till

        # no same root
        if same_till == 0:
            return False

        # same level but different branches
        if len(id1) - same_till > 2:
            return False

        # determine which one is input and which one is output
        if len_diff:
            obj0_type = obj0.get_local()
        else:
            obj0_type = obj0.get_global()
        obj1_type = obj1.get_global()

        # cant connect if both have same type (i.e. Input-Input or Output-Output)
        if obj0_type == obj1_type:
            return False

        input = None
        output = None
        if obj0_type == ConnectableFlag.INPUT:
            input, output = obj0, obj1
        else:
            input, output = obj1, obj0

        def _connect(parent):
            Connectable.connect(input, output)
            if not parent.is_allowed():
                Connectable.disconnect(input, output)


        parent_id = id0[:same_till]
        if parent_id != self.identifier():
            parent = self.find(parent_id)
            if not parent:
                return False
            return _connect(parent)

        return _connect(self)


    def update(self) -> bool:
        changed = self.inputs.update()

        if changed:
            self.process()

        changed = self.outputs.update()
        return changed
