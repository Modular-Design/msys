from pymsys import ILink, IMetadata, IConnectable, INode, IConnection
from pymsys import Connectable, Option, Node, UUIDGenerator, UpdatableChildList
from typing import Dict, Optional, List

from ..generators import RegisterGenerator

from ..interfaces import IModule
from .remote_node import RemoteNode

from ..core import Registration, Priority, Connection


class Module(Node, IModule):
    def __init__(self,
                 meta: Optional[IMetadata] = None,
                 inputs: Optional[Dict[str, IConnectable]] = None,
                 outputs: Optional[Dict[str, IConnectable]] = None,
                 options: Optional[Dict[str, Option]] = None,
                 nodes: Optional[Dict[str, INode]] = None,
                 connections: Optional[List[IConnection]] = None,
                 ram_reserve: Optional[float] = 0.0,
                 registration: Optional[Registration] = None,
                 parent: Optional[ILink] = None,
                 **kwargs):

        self.registration = registration
        self.nodes = UpdatableChildList(
            nodes,
            RegisterGenerator(
                register=registration,
                generated_class=RemoteNode,
                generate_name=False,
            )
        )
        self.connections = UpdatableChildList(
            connections,
            UUIDGenerator(
                generated_class=Connection,
                generate_name=False,
            )
        )
        super().__init__(
            meta=meta,
            inputs=inputs,
            outputs=outputs,
            options=options,
            input_generator=UUIDGenerator(default_class=Connectable, generate_name=False),
            output_generator=UUIDGenerator(default_class=Connectable, generate_name=False),
            option_generator=UUIDGenerator(default_class=RemoteNode, generate_name=False),
            ram_reserve=ram_reserve,
            parent=parent,
            nodes=self.nodes,
            connections=self.connections,
            **kwargs
        )

    def get_nodes(self) -> UpdatableChildList:
        return self.nodes

    def form_tree(self) -> bool:
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

    def launch(self, key: str):
        if not self.registration:
            return False

        node = self.registration.launch(key)
        node.set_parent(self)
        self.add_node(node)  # TODO remove id setter
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

        if c0type == "inputs":
            input = connectable0
            output = connectable1
        else:
            input = connectable1
            output = connectable0

        return dict(output=output, input=input)

    def connect(self, output: "Connectable", input: "Connectable") -> bool:
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

    def process(self, input_changed: bool):
        if not input_changed:
            return True
        """
        solve all nodes
        """

        priorities = [Priority(n) for n in self.nodes]

        priorities.sort()
        if self.form_tree():
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
