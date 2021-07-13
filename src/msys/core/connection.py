import weakref
from .unit import Unit, UUnit
from .connectable import Connectable, ConnectableInterface, ConnectableFlag
import json
from typing import Optional
import uuid
from ..interfaces import ISerializer

class Connection(Child):
    def __init__(self,
                 parent: "Module",
                 output: Optional[Connectable] = None,
                 input: Optional[Connectable]  = None,
                 id: Optional[str] =None):

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


    def load(self, json: dict) -> bool:
        if not super().from_dict(json):
            return False
        if self.out_ref() is None:
            self.out_ref = weakref.ref(parent.find(json.keys()[0]))
        elif json.dumps(self.out_ref().complete_id()) == json.keys()[0]:
            self.out_ref = weakref.ref(parent.find(json.keys()[0]))

        json = json.get(json.dumps(self.out_ref().complete_id()))
        if not json:
            return False
        if self.in_ref() is None:
            self.in_ref = weakref.ref(parent.find(json.keys()[0]))
        elif json.dumps(self.in_ref().complete_id()) == json.keys()[0]:
            self.in_ref = weakref.ref(parent.find(json.keys()[0]))

        config = json.get(json.dumps(self.in_ref().complete_id()))

        Child.load(self, config)
        if "meta" in config.keys():
            self.meta = config["meta"]
        return True

    @staticmethod
    def find_connection(root:Unit, obj0, obj1) -> []:
        """

        Oberride this function
        Returns:
            [closest_parent, input, output]
        """
        if isinstance(obj0, list):
            obj0 = root.find(obj0)

        if isinstance(obj1, list):
            obj1 = root.find(obj1)
        if not (issubclass(obj0.__class__,
                           ConnectableInterface) and issubclass(obj1.__class__,
                                                                ConnectableInterface)):
            return []

        id0 = obj0.complete_id()
        id1 = obj1.complete_id()
        len_diff = len(id1) - len(id0)

        if abs(len_diff) > 1:
            return []

        if len_diff < 0:
            obj1, obj0 = obj0, obj1
            id0 = obj0.complete_id()
            id1 = obj1.complete_id()
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
            po_diff = len(obj.complete_id()) - len(p_id)
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

        return [output, input, root.find(parent_id)]

    @staticmethod
    def search_connect(parent, output, input) -> bool:
        res = Connection.find_connection(parent, output, input)
        return Connection.connect(res[0], res[1], res[2])

    @staticmethod
    def connect(output: ConnectableInterface, input : ConnectableInterface, parent=None) -> bool:
        if not (issubclass(input.__class__, ConnectableInterface) and issubclass(output.__class__,
                                                                                 ConnectableInterface)):
            return False

        if not input.get_type().is_connectable(output.get_type()):
            return False

        if parent:
            if parent.is_protected():
                return False

        ingoing = input.get_ingoing()
        if ingoing:
            if not input.disconnect_ingoing():
                return False
        input.input_ref = weakref.ref(output)

        outgoing = output.get_outgoing()
        if not input in outgoing:
            output.inputs_refs.append(weakref.ref(input))

        if parent:
            Connection(parent, output, input)

        return True

    @staticmethod
    def search_disconnect(parent, output, input) -> bool:
        res = Connection.find_connection(parent, output, input)
        return Connection.disconnect(res[0], res[1])

    @staticmethod
    def disconnect(output: ConnectableInterface,  input:ConnectableInterface) -> bool:
        if not (issubclass(Connectable, input.__class__) and issubclass(Connectable, output.__class__)):
            return False

        if not input in output.get_outgoing():
            return False
        input.input_ref = None
        index = output.get_outgoing().index(input)
        output.inputs_refs.pop(index)
        return True