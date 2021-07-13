from .node import Node
from ..interfaces import IModule, INode, IChild
from .child import Child
from .metadata import Metadata
from .connectable import Connectable, ConnectableFlag, IConnectable
from .connection import Connection
from .option import Option
from .helpers import load_entrypoints
from .priority import Priority
from msys.management import Registration

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
        self.meta = Metadata(name=name, description=description)

        self.registration = registration

        # add nodes
        if nodes is None:
            nodes = []
        self.nodes = []

        for node in nodes:
            if isinstance(node, Node):
                self.nodes.append(node)
            if type(node) == str:
                self.launch(node)

        self.connections = []

    def add_input(self) -> bool:
        raise NotImplementedError

    def add_output(self) -> bool:
        raise NotImplementedError

    def are_inputs_removable(self) -> bool:
        raise NotImplementedError

    def are_outputs_removable(self) -> bool:
        raise NotImplementedError

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
        raise NotImplementedError

    def get_node(self, id:str):
        if id == self.id:
            return self
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def get_nodes(self) -> List[INode]:
        raise self.nodes

    def get_options(self) -> List["Option"]:
        raise NotImplementedError

    def get_output(self, id: str, local=False):
        raise NotImplementedError

    def get_outputs(self, local=False) -> List[IConnectable]:
        raise NotImplementedError

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

        node = self.registration.launch_blueprint(key)
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

