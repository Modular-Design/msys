from .node import Node
from ..interfaces import IModule, INode, IChild
from .child import Child
from .metadata import Metadata
from .connectable import Connectable, ConnectableFlag, IConnectable
from .connection import Connection
from .option import Option
from .helpers import load_entrypoints
from .priority import Priority
from msys.core.registration import Registration

from typing import Optional, List

from dataclasses import dataclass





class Module(Child, IModule):
    def __init__(self,
                 # Child
                 parent: Optional["Module"] = None,
                 id: Optional[str] = None,

                 # Metadata
                 name: Optional[str] = "Module",
                 description: Optional[str] = "A Master-Module",

                 # new
                 inputs: Optional[List[Connectable]] = None,
                 outputs: Optional[List[Connectable]] = None,
                 options: Optional[List[Option]] = None,
                 removable_inputs: Optional[bool] = False,
                 removable_outputs: Optional[bool] = False,
                 ram_reserve: Optional[float] = 0.0,
                 nodes: Optional[INode] = None,
                 connections: Optional[List[Connection]] = None,
                 registration: Optional[Registration] = None,
                 ):

        super().__init__(parent, id)
        self.ram_reserve = 20
        self.meta = Metadata(name=name, description=description)

        self.registration = registration

        # add inputs
        if inputs is None:
            inputs = []
        self.inputs = inputs

        # add outputs
        if outputs is None:
            outputs = []
        self.outputs = outputs

        # add options
        if options is None:
            options = []
        self.options = options

        # add nodes
        if nodes is None:
            nodes = []
        self.nodes = nodes

        for node in nodes:
            if isinstance(node, Node):
                self.nodes.append(node)
            if type(node) == str:
                self.launch(node)

        self.connections = []

    def to_dict(self) -> dict:
        # self.update_inverted()
        res = Child.to_dict(self)
        print("[Module] to_dict: " + str(res))

        removable = self.is_editable()

        res["ram"] = self.ram_reserve
        res["meta"] = self.meta.to_dict()

        res["options"] = {"size": len(self.options), "removable": removable, "elements": []}
        if self.options:
            for opt in self.options:
                res["options"]["elements"].append(opt.to_dict())

        res["inputs"] = {"size": len(self.inputs), "removable": removable, "elements": []}
        if self.inputs:
            for inp in self.inputs:
                res["inputs"]["elements"].append(inp.to_dict())

        res["outputs"] = {"size": len(self.outputs), "removable": removable, "elements": []}
        if self.outputs:
            for out in self.outputs:
                res["outputs"]["elements"].append(out.to_dict())

        res["nodes"] = {"size": len(self.nodes), "removable": removable, "elements": []}
        if self.nodes:
            for node in self.nodes:
                res["nodes"]["elements"].append(node.to_dict())

        res["connections"] = {"size": len(self.connections), "removable": True, "elements": []}
        if self.connections:
            for connection in self.connections:
                res["connections"]["elements"].append(connection.to_dict())
        return res

    def load(self, dictionary: dict) -> bool:
        Child.load(self, dictionary)

        if "meta" in dictionary.keys():
            if not self.meta.to_dict():
                self.meta.load(dictionary["meta"])

        if "options" in dictionary.keys():
            options = dictionary["options"]

            for opt in options["elements"]:
                for option in self.options:
                    if option.id == opt["id"]:
                        if not option.load(opt):
                            return False
                        break

        if "inputs" in dictionary.keys():
            inputs = dictionary["inputs"]
            for inp in inputs["elements"]:
                found = False
                for input in self.inputs:
                    if input.id == inp["id"]:
                        if not input.load(inp):
                            return False
                        found = True
                        break
                if not found:
                    con = Connectable(parent=self, flag=ConnectableFlag.INPUT, id=out["id"])
                    con.load(inp)
                    self.inputs.append(con)

            diff = len(self.inputs) - inputs["size"]
            if diff > 0:
                for input in self.inputs:
                    found = False
                    for inp in inputs["elements"]:
                        if input.id == inp["id"]:
                            found = True
                            break
                    if not found:
                        self.inputs.remove(input)

        if "outputs" in dictionary.keys():
            outputs = dictionary["outputs"]
            for out in outputs["elements"]:
                found = False
                for output in self.outputs:
                    if output.id == out["id"]:
                        if not output.load(out):
                            return False
                        found = True
                        break
                if not found:
                    con = Connectable(parent=self, flag=ConnectableFlag.OUTPUT, id=out["id"])
                    con.load(out)
                    self.outputs.append(con)

            diff = len(self.outputs) - outputs["size"]
            if diff > 0:
                for output in self.outputs:
                    found = False
                    for out in outputs["elements"]:
                        if output.id == out["id"]:
                            found = True
                            break
                    if not found:
                        self.outputs.remove(output)

        return True


    def add_input(self) -> bool:
        raise NotImplementedError

    def add_output(self) -> bool:
        raise NotImplementedError

    def is_editable(self) -> bool:
        return not bool(self.id)

    def are_inputs_removable(self) -> bool:
        return self.is_editable()

    def are_outputs_removable(self) -> bool:
        return self.is_editable()

    def find_child(self, cid: List[str], local=False) -> IChild:
        if self.get_global_id() == cid:
            return self

        def get_matches(clist: list):
            for i in range(len(clist)):
                if clist[i] != cid[i]:
                    return i


        matches = get_matches(self.get_global_id())

        childs = self.inputs + self.outputs
        for child in childs:
            if child.get_global_id() == cid:
                return child

        if not local:
            for child in childs:
                match = get_matches(child.get_global_id())
                if match > matches:
                    return child.find_child(cid)


    def get_input(self, id: str, local=False):
        raise NotImplementedError

    def get_inputs(self, local=False) -> List[IConnectable]:
        if not local:
            return self.outputs
        return self.inputs

    def get_name(self) -> str:
        return self.meta.name

    def get_description(self) -> str:
        return self.meta.description

    def set_name(self, name: str):
        self.meta.name = name

    def set_description(self, description: str):
        self.meta.description = description

    def get_node(self, id:str):
        if id == self.id:
            return self
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def get_nodes(self) -> List[INode]:
        return self.nodes

    def get_options(self) -> List["Option"]:
        return self.options

    def get_output(self, id: str, local=False):
        raise NotImplementedError

    def get_outputs(self, local=False) -> List[IConnectable]:
        if not local:
            return self.inputs
        return self.outputs

    def get_removable_inputs(self) -> List[IConnectable]:
        raise NotImplementedError

    def get_removable_outputs(self) -> List[IConnectable]:
        raise NotImplementedError

    def is_changed(self) -> bool:
        raise NotImplementedError

    def form_linear(self) -> bool:
        """
        Checks if connections between Nodes are definitly solveable in linear time.
        (Only one time to update all)

        Returns:
            bool: true if connections form linear tree like shape
        """
        for i in range(len(self.nodes)):
            run = []

            def move_from(node) -> bool:
                run.append(node)
                outputs = node.get_outputs()
                for out in outputs:
                    for input in out.get_inputs():
                        parent = input.get_parent()
                        # prevent from going outside
                        if parent not in self.nodes:
                            continue

                        # preventing double findings
                        if parent in run:
                            # if circle
                            if parent is self.nodes[i]:
                                return False
                            continue

                        if not move_from(parent):
                            return False
                return True

            if not move_from(self.nodes[i]):
                return False
        return True

    def remove_input(self, id) -> bool:
        raise NotImplementedError

    def remove_output(self, id) -> bool:
        raise NotImplementedError

    def update(self) -> bool:
        changed = self.inputs.update()

        if changed:
            self.solve()

        changed = self.outputs.update()
        return changed

    def add_node(self,
                 node: Node):
        self.nodes.append(node)

    def launch(self, key: str):
        if not self.registration:
            return False

        node = self.registration.launch(key)
        node.set_parent(self)
        self.add_node(node) # TODO remove id setter
        return True

    def connect_via_ids(self, id0: "Connectable", id1: "Connectable"):

        return True

    def identify_connectable_type(self, connectable0: "Connectable", connectable1: "Connectable"):
        input = None
        output = None

        c0type = None
        if connectable0.get_parent() is self:
            c0type = connectable0.get_local()
        else:
            c0type = connectable0.get_global()

        c1type = None
        if connectable1.get_parent() is self:
            c1type = connectable1.get_local()
        else:
            c1type = connectable1.get_global()

        if c0type == c1type:
            return []

        if c0type == ConnectableFlag.INPUT:
            input = connectable0
            output = connectable1
        else:
            input = connectable1
            output = connectable0

        return dict(output=output, input=input)

    def connect(self,  output: "Connectable", input: "Connectable") -> bool:
        if Connection(self, output, input) is None:
            return True
        return False

    def disconnect(self, cid: List[str]) -> bool:
        for i in range(len(self.connections)):
            connection = self.connections[i]
            if connection.get_global_id() == cid:
                connection.disconnect()
                return True
        return False


    def solve(self) -> bool:
        """
        solve all nodes
        """

        priorities = [Priority(n) for n in self.nodes]

        priorities.sort()
        if self.is_tree():
            for p in priorities:
                p.update()
            return True

        # solve complex graph
        iteration = 0
        max_iterations = 500
        start_from = 0
        group_changed = True

        while group_changed:
            if iteration > max_iterations:
                break
            ++ iteration
            group_changed = False
            for position in range(start_from, len(priorities)):
                node = priorities[position]
                if node.update():
                    group_changed = True

                # ignore modules which can change only once in the future
                if node.inputs == 0:
                    start_from = position
                if not (position + 1 < len(priorities)):
                    continue

                # equal loop branches
                if priorities[position].inputs == priorities[position + 1].inputs:
                    # register inflicted changes
                    for p in priorities:
                        p.update_numbers()

                    dynamic = priorities[start_from:]
                    dynamic.sort()
                    priorities = priorities[:start_from] + dynamic
        return True

