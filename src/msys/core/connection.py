import weakref
from pymsys import ISerializer, IConnectable, Connectable, Link

import json
from typing import Optional
import uuid


class Connection(Link):
    def __init__(self,
                 parent: Optional["Module"],
                 output: Optional[Connectable] = None,
                 input: Optional[Connectable] = None, ):

        if not input.is_connectable(output):
            return None
        input.set_ingoing(output)
        output.add_outgoing(input)
        super().__init__(parent, id)
        self.out_ref = weakref.ref(output)
        self.out_id = []
        self.in_ref = weakref.ref(input)
        self.in_id = []
        self.meta = []

        self.parent.connections.append(self)

    def get_input(self):
        input = self.in_ref()
        if input:
            return input

        # reconnecting
        input = self.parent.find(self.in_id)
        if not input:
            self.disconnect()
            return None
        if isinstance(input, IConnectable):
            input.set_ingoing(self)
            self.in_ref = weakref.ref(input)
            return input
        return None

    def get_output(self):
        output = self.out_ref()
        if output:
            return output

        # reconnecting
        output = self.parent.find(self.out_id)
        if not output:
            self.disconnect()
            return None
        if isinstance(output, IConnectable):
            output.add_outgoing(self)
            self.out_ref = weakref.ref(output)
            return output
        return None

    def disconnect(self):
        input = self.in_ref()
        output = self.out_ref()

        if input:
            input.set_ingoing(None)

        if output:
            output.remove_outgoing(self)

        self.parent.connections.remove(self)

    def to_dict(self) -> dict:
        config = Child.to_dict(self)
        config["meta"] = self.meta
        input = self.get_input()
        output = self.get_output()

        if input is None or output is None:
            self.disconnect()
            return None
        return {json.dumps(output.complete_id()): {json.dumps(input.complete_id()): config}}

    def load(self, config: dict) -> bool:
        if not super().from_dict(config):
            return False
        if self.out_ref() is None:
            self.out_ref = weakref.ref(config.find(config.keys()[0]))
        elif json.dumps(self.out_ref().complete_id()) == config.keys()[0]:
            self.out_ref = weakref.ref(parent.find(config.keys()[0]))

        config = config.get(json.dumps(self.out_ref().complete_id()))
        if not config:
            return False
        if self.in_ref() is None:
            self.in_ref = weakref.ref(parent.find(config.keys()[0]))
        elif json.dumps(self.in_ref().complete_id()) == config.keys()[0]:
            self.in_ref = weakref.ref(parent.find(config.keys()[0]))

        config = config.get(json.dumps(self.in_ref().complete_id()))

        Child.load(self, config)
        if "meta" in config.keys():
            self.meta = config["meta"]
        return True
