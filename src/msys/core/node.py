from .processor import Processor

from ..interfaces import INode
from .child import Child, IChild
from .metadata import Metadata
from typing import Optional, List
from .connectable import Connectable, ConnectableFlag
from .option import Option


class Node(Child, INode):
    def __init__(self,
                 # new
                 process: Processor,

                 # Child
                 parent: Optional["Module"] = None,
                 id: Optional[str] = None,

                 # Metadata
                 name: Optional[str] = None,
                 description: Optional[str] = None,

                 # new
                 ram_reserve: Optional[float] = 0.0,
                 ):


        self.process = process

        super().__init__(parent, id)

        self.options = []
        self.inputs = []
        self.outputs = []
        self.removable_inputs = False
        self.removable_outputs = False
        self.ram_reserve = ram_reserve
        self.meta = Metadata(name=name, description=description)

        self.load(self.process.get_config())

    def get_name(self) -> str:
        return self.meta.name

    def get_description(self) -> str:
        return self.meta.description

    def set_name(self, name: str):
        self.meta.name = name

    def set_description(self, description: str):
        self.meta.description = description

    def get_processor(self) -> Processor:
        return process

    def get_configuration(self) -> dict:
        """
        Returns:
            dict: header config without input or output specific content
        """
        res = dict()
        res["ram"] = self.ram_reserve
        res["meta"] = self.meta.to_dict()

        res["options"] = {"size": len(self.options), "removable": False, "elements": []}
        if self.options:
            for opt in self.options:
                res["options"]["elements"].append(opt.to_dict())

        res["inputs"] = {"size": len(self.inputs), "removable": self.removable_inputs, "elements": []}

        res["outputs"] = {"size": len(self.outputs), "removable": self.removable_outputs, "elements": []}

        return res


    def to_dict(self) -> dict:
        self.update_inverted()
        res = Child.to_dict(self)
        print("[Node] to_dict: " + str(res))
        res.update(self.get_configuration())

        if self.inputs:
            for inp in self.inputs:
                res["inputs"]["elements"].append(inp.to_dict())

        if self.outputs:
            for out in self.outputs:
                res["outputs"]["elements"].append(out.to_dict())

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


    def configure(self, data: dict) -> bool:
        """
        shortcut
        Args:
            data:

        Returns:

        """
        return self.load(
            self.process.change_config(data)
        )

    def update_inverted(self):
        for c in self.inputs:
            c.meta.inverted = self.meta.inverted

        for c in self.outputs:
            c.meta.inverted = self.meta.inverted

    def update(self) -> bool:
        for inp in self.inputs:
            if inp.update():
                pass

        self.load(self.process.update_config(self.to_dict()))

        for out in self.outputs:
            if out.update():
                pass

    def is_changed(self) -> bool:
        for inp in self.inputs:
            if inp.is_changed():
                return True

        for out in self.outputs:
            if out.is_changed():
                return True

    """
    
    INode
    
    """

    def find_child(self, cid: List[str], local=False) -> IChild:
        if self.get_global_id() == cid:
            return self
        childs = self.inputs +self.outputs
        for child in childs:
            if child.get_global_id() == cid:
                return child
        return None

    def get_inputs(self, local=False) -> List["Connectable"]:
        if not local:
            return self.outputs
        return self.inputs

    def get_outputs(self, local=False) -> List["Connectable"]:
        if not local:
            return self.inputs
        return self.outputs

    def get_input(self, id: str, local = False):
        for con in self.get_inputs(local):
            if con.id == id:
                return con
        return None

    def get_output(self, id: str, local = False):
        for con in self.get_outputs(local):
            if con.id == id:
                return con
        return None

    def get_options(self) -> List["Option"]:
        return self.options

    def are_inputs_removable(self) -> bool:
        return self.removable_inputs

    def are_outputs_removable(self) -> bool:
        return self.removable_outputs

    def get_removable_inputs(self) -> List["Connectable"]:
        res = []
        for connectable in self.inputs:
            if connectable.is_removable():
                res.append(connectable)
        return res

    def get_removable_outputs(self) -> List["Connectable"]:
        res = []
        for connectable in self.outputs:
            if connectable.is_removable():
                res.append(connectable)
        return res

    def add_input(self) -> bool:
        data = self.to_dict()
        data["inputs"] = {"size": len(self.inputs) + 1, "removable": self.removable_inputs, "elements": []}
        return self.configure(data)

    def remove_input(self, id) -> bool:
        input = self.get_input(id)
        if input is None:
            return False

        self.inputs.remove(input)

        data = self.to_dict()
        return self.configure(data)

    def add_output(self) -> bool:
        data = self.to_dict()
        data["outputs"] = {"size": len(self.outputs) + 1, "removable": self.removable_outputs, "elements": []}
        return self.configure(data)

    def remove_output(self, id) -> bool:
        output = self.get_output(id)
        if output is None:
            return False

        self.outputs.remove(output)

        data = self.to_dict()
        return self.configure(data)


    def exit(self):
        del self
        # if self.process is not None:
        #    self.process.kill()
        pass
