from .serializer_collections import ConnectableList
from .connectable import ConnectableFlag, Connectable
from .registrable import Registrable
from .unit import UUnit
from .connection import Connection



class Module(UUnit, Registrable):
    def __init__(self, inputs=[], outputs=[], options=[], sub_modules=[], id=None):
        self.inputs = ConnectableList(self, inputs, ConnectableFlag.INPUT)
        self.outputs = ConnectableList(self, outputs, ConnectableFlag.OUTPUT)
        self.options = options
        self.modules = []
        self.connections = []
        for module in sub_modules:
            self.add_module(module)

        super().__init__(id)
        Registrable.__init__(self)

    def get_inputs(self):
        return list(self.inputs)

    def get_outputs(self):
        return list(self.outputs)

    def get_options(self):
        return self.options

    def get_childs(self) -> []:
        return self.inputs[:] + self.outputs[:] + self.modules + self.connections

    def add_module(self, module: UUnit):
        module.parent = self
        self.modules.append(module)

    def set_inverted(self, inverted: bool):
        super().set_inverted(inverted)
        for i in inputs:
            i.set_inverted(inverted)
        for o in outputs:
            o.set_inverted(inverted)

    def to_dict(self) -> dict:
        res = UUnit.to_dict(self)
        res.update(Registrable.to_dict(self))

        if self.options:
            options = []
            for o in self.options:
                options.append(o.to_dict())
            res["options"] = options

        if self.inputs[:]:
            res["inputs"] = self.inputs.to_dict()

        if self.outputs[:]:
            res["outputs"] = self.outputs.to_dict()

        if self.modules:
            res["modules"] = []
            for module in self.modules:
                res["modules"].append(module.to_dict())

        if self.connections:
            res["connections"] = {}
            for c in self.connections:
                json = c.to_dict()
                if json is None:
                    continue
                key = list(json.keys())[0]
                json.values
                if key in res["connections"].keys():
                    res["connections"][key].update(list(json.values())[0])
                else:
                    res["connections"].update(json)

        return res

    def from_dict(self, json: dict, safe=False) -> bool:
        def _from_dict(key, lists, changeable=False):
            connectables = json[key]
            for new_c in connectables:
                if not "id" in new_c:
                    break
                for old_c in lists:
                    if new_c["id"] == old_c.id:
                        old_c.from_dict(new_c, safe)
                        break

        if safe and parent.is_protected():
            return False

        if "options" in json.keys():
            _from_dict("options", self.options)

        if not UUnit.from_dict(self, json, safe=False):
            return False

        Registrable.from_dict(self, json)


        if "inputs" in json.keys():
            self.inputs.from_dict(json["inputs"])

        if "outputs" in json.keys():
            self.outputs.from_dict(json["outputs"])

        return True

    def process(self) -> bool:
        """
        Overide this methode!
        Describs inner proccesing.
        """

        def eval_tim_score(module, dtime):
            if dtime <= 1:
                dtime = 1
            import math
            module.time_score = round(math.log10(dtime))

        def prioritize(priorities, complexity=0):
            if complexity == 0:
                return sorted(priorities, key=lambda module: (module.inputs.get_no_connected(),
                                                            -module.outputs.get_no_connected()))
            if complexity == 1:
                # priority by:
                # lower connected inputs
                # then lower time score
                # then lowest change counter: connected inputs - input changes
                # then highest changes
                # then highest output connections
                return sorted(priorities, key=lambda module: (
                    module.inputs.get_no_connected(),
                    module.time_score,
                    module.inputs.get_no_connected() - module.inputs.get_no_changed(),
                    -module.inputs.get_no_changed(),
                    module.outputs.get_no_connected()))
            return []

        self.modules = prioritize(self.modules)
        if self.is_tree():
            for m in self.modules:
                m.update()
            return True

        # solve complex graph
        iteration = 0
        max_iterations = 500
        start_from = 0
        group_changed = True
        priority_list = self.modules.copy()
        while group_changed:
            if iteration > max_iterations:
                break
            ++ iteration
            group_changed = False
            for m_id in range(start_from, len(priority_list)):
                module = priority_list[m_id]
                import time
                start = time.time()
                changed = module.update()
                delta_time = time.time() - start
                eval_tim_score(module, delta_time)
                if changed:
                    group_changed = True

                # ignore modules which can change only once in the future
                if module.inputs.get_no_connected() == 0:
                    start_from = m_id
                if not (m_id + 1 < len(self.modules)):
                    continue
                # TODO ignore if connected inputs are 0?
                if priority_list[m_id].inputs.get_no_connected() == priority_list[m_id + 1].inputs.get_no_connected():
                    # register inflicted changes
                    for m in priority_list:
                        m.inputs.update_numbers()

                    priority_list = priority_list[:start_from] + prioritize(priority_list[start_from:], 1)
        return True

    def is_tree(self) -> bool:
        """


        """
        for i in range(len(self.modules)):
            run = []

            def move_from(module) -> bool:
                run.append(module)
                outputs = module.get_outputs()
                for out in outputs:
                    for input in out.get_outgoing():
                        parent = input.parent
                        # prevent from going outside
                        if parent not in self.modules:
                            continue
                        # preventing double findings
                        if parent in run:
                            # if circle
                            if parent is self.modules[i]:
                                return False
                            continue

                        if not move_from(parent):
                            return False
                return True

            if not move_from(self.modules[i]):
                return False
        return True


    def connect(self, obj0, obj1) -> bool:
        res = Connection.find_connection(self, obj0, obj1)
        if not res:
            return False

        return Connection.connect(res[0], res[1], res[2])

    def update(self) -> bool:
        changed = self.inputs.update()

        if changed:
            self.process()

        changed = self.outputs.update()
        return changed

    def delete(self):
        if self.parent is not None:
            self.parent.modules.remove(self)