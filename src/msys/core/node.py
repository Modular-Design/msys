import requests
from ..interfaces import IChild, IUpdatable, ISerializer
from typing import Optional, List
import subprocess
from .metadata import Metadata
import json
from .connectable import Connectable
from .option import Option
from .processor import Processor
import uuid


class Node(IChild, IUpdatable, ISerializer):
    def __init__(self,
                 id: Optional[str] = None,
                 process: Optional[str] = None,
                 url: Optional[str] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 inputs: Optional[List[Connectable]] = None,
                 outputs: Optional[List[Connectable]] = None,
                 options: Optional[List[Option]] = None,
                 removable_inputs: Optional[bool] = False,
                 removable_outputs: Optional[bool] = False,
                 ram_reserve: Optional[float] = 0.0,
                 ):

        if process:
            self.process = Processor(process)
            self.url = self.process.start()
            print("[Node]: url "+ self.url)

        else:
            self.url = url

        self.parent = None

        if id is None:
            id = str(uuid.uuid4())

        self.id = id
        self.meta = Metadata(name=name, description=description)

        if options is None:
            options = []
        self.options = options

        if inputs is None:
            inputs = []
        self.inputs = inputs

        if outputs is None:
            outputs = []
        self.outputs = outputs

        self.removable_inputs = False
        self.removable_outputs = False
        self.ram_reserve = ram_reserve

        if self.url:
            response = requests.get(self.url + "/config")
            if response.status_code != 200:
                pass

            self.load(response.content)
        return

    def set_parent(self, module: "Module"):
        self.parent = module

    def get_configuration(self) -> dict:
        res = dict()
        res["id"] = self.id
        res["ram"] = self.ram_reserve
        res["meta"] = self.meta.to_dict()

        if self.options:
            res["options"] = {"size": len(self.options), "addable": False, "elements": []}
            for opt in self.options:
                res["options"]["elements"].append(opt.to_dict())

        if self.inputs:
            res["inputs"] = {"size": len(self.inputs), "removable": self.removable_inputs, "elements": []}

        if self.outputs:
            res["outputs"] = {"size": len(self.outputs), "removable": self.removable_outputs, "elements": []}

    def to_dict(self) -> dict:
        self.update_inverted()
        res = self.get_configuration()

        if self.inputs:
            for inp in self.inputs:
                res["inputs"]["elements"].append(inp.to_dict())

        if self.outputs:
            for out in self.outputs:
                res["outputs"]["elements"].append(out.to_dict())

        return res

    def configure(self, data: dict) -> bool:
        print("[Node] type: " + str(type(data)))
        response = requests.post(self.url + "/config", data)
        print("[Node] response")
        if response.status_code != 200:
            return False
        print("[Node] configure")
        return self.load(response.content)

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

    def load(self, dictionary: dict) -> bool:
        if type(dictionary) == str or type(dictionary) == bytes:
            dictionary = json.loads(dictionary)

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
                    con = Connectable(parent=self)
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
                    con = Connectable(parent=self, input=False)
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

    def update_inverted(self):
        for c in self.inputs:
            c.meta.inverted = self.meta.inverted

        for c in self.outputs:
            c.meta.inverted = self.meta.inverted

    def update(self) -> bool:
        for inp in self.inputs:
            if inp.update():
                pass

        response = requests.put(self.url + "/update")
        if response.status_code != 200:
            pass

        self.load(response.content)

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

    def get_input(self, id: str):
        for con in self.inputs:
            if con.id == id:
                return con
        return None

    def get_output(self, id: str):
        for con in self.outputs:
            if con.id == id:
                return con
        return None

    def update_inputs(self):
        pass

    def update_outputs(self):
        pass

    def exit(self):
        del self
        # if self.process is not None:
        #    self.process.kill()
        pass
