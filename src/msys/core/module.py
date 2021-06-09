from .interfaces import ConnectableInterface
from .serializer_lists import ConnectableList
from .connectable import ConnectableFlag, Connectable
from .registrable import Registrable
from .unit import Unit
import uuid


class Module(Unit, Registrable):
    def __init__(self, inputs=[], outputs=[], options=[], sub_modules=[], id=None):
        self.inputs = ConnectableList(self, inputs, ConnectableFlag.INPUT)
        self.outputs = ConnectableList(self, outputs, ConnectableFlag.OUTPUT)
        self.options = options
        self.modules = []
        self.connections = {}
        for module in sub_modules:
            self.add_module(module)

        if id is None:
            id = str(uuid.uuid4())
        super().__init__(id)
        Registrable.__init__(self)

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
        res.update(Registrable.to_dict(self))

        options = []
        for o in self.options:
            options.append(o.to_dict())
        res["options"] = options

        res["inputs"] = self.inputs.to_dict()

        res["outputs"] = self.outputs.to_dict()

        res["modules"] = []
        for module in self.modules:
            res["modules"].append(module.to_dict())

        res["connections"] = self.connections

        return res

    def from_dict(self, json: dict) -> bool:
        found = super().from_dict(json)
        if Registrable.from_dict(self, json):
            found = True

        def _from_dict(key, lists, changeable=False):
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
            found = True

        if "inputs" in json.keys():
            self.inputs.from_dict(json["inputs"])
            found = True

        if "outputs" in json.keys():
            self.outputs.from_dict(json["outputs"])
            found = True

        return found

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

    def is_connection_allowed(self) -> bool:
        """

        Oberride this function
        Returns:

        """
        return True

    def find_pair(self, obj0, obj1) -> []:
        """

        Oberride this function
        Returns:
            [closest_parent, input, output]
        """
        if obj0 is list:
            obj0 = self.find(obj0)
        if obj1 is list:
            obj0 = self.find(obj1)
        if not (issubclass(obj0.__class__,
                           ConnectableInterface) and issubclass(obj1.__class__,
                                                                ConnectableInterface)):
            return []

        id0 = obj0.identifier()
        id1 = obj1.identifier()
        len_diff = len(id1) - len(id0)
        if abs(len_diff) > 1:
            return []

        if len_diff < 0:
            obj1, obj0 = obj0, obj1
            id0 = obj0.identifier()
            id1 = obj1.identifier()
        # obj0 is higher or level with obj1

        # number of same levels
        same_till = 0
        for i in range(len(id0)):
            if id0[i] != id1[i]:
                break
            same_till += 1

        # no same root
        if same_till == 0:
            return []

        # same level but different branches
        if len(id1) - same_till > 2:
            return []

        parent_id = id0[:same_till]

        # determine which one is input and which one is output
        def get_type(p_id, obj):
            po_diff = len(obj.identifier()) - len(p_id)
            if po_diff == 1:
                return obj.get_local()
            elif po_diff == 2:
                return obj.get_global()
            else:
                return None

        obj0_type = get_type(parent_id, obj0)
        if not obj0_type:
            return []

        obj1_type = get_type(parent_id, obj1)
        if not obj1_type:
            return []

        # cant connect if both have same type (i.e. Input-Input or Output-Output)
        if obj0_type == obj1_type:
            return []

        input = None
        output = None
        if obj0_type == ConnectableFlag.INPUT:
            input, output = obj0, obj1
        else:
            input, output = obj1, obj0

        return [self.find(parent_id), input, output]

    @staticmethod
    def create_connection(parent, output, input) -> bool:
        if not parent.is_connection_allowed():
            return False

        Connectable.connect(output, input)
        import json
        key = json.dumps(output.identifier())
        content = {json.dumps(input.identifier()): []}
        if key in parent.connections.keys():
            parent.connections[json.dumps(output.identifier())].update(content)
        else:
            parent.connections[json.dumps(output.identifier())] = content

        return True

    def connect(self, obj0, obj1) -> bool:
        res = self.find_pair(obj0, obj1)
        if not res:
            return False

        return Module.create_connection(res[0], res[2], res[1])

    def update(self) -> bool:
        changed = self.inputs.update()

        if changed:
            self.process()

        changed = self.outputs.update()
        return changed
