from .processor import Processor
from .helpers import load_entrypoints
from pymsys import INode
import urllib
from pathlib import Path
import json
from typing import Optional, List


class Registration:
    def __init__(self,
                 storefile: Optional[str] = None,
                 sources: Optional[str] = None):

        if sources is None:
            sources = []

        if not storefile:
            self.storefile = "resources.json"
        self.sources = sources + [self.storefile]
        self.resources = dict()  # {"id": "name", "description",
        # "config" or
        # "location", "limit":int or
        # "remote",
        # "instances" ["Process1", "Process2", etc.]}
        self.load()

    def get_registered(self, exclude: Optional[List[str]] = None) -> dict:
        "use for printing"
        res = dict()
        for key in self.resources.keys():
            own = dict()
            resource = self.resources[key]

            if exclude:
                ignore = False
                for exept in exclude:
                    if exept in resource.keys():
                        ignore = True
                        break
                if ignore:
                    continue

            if "name" in resource.keys():
                own["name"] = resource["name"]

            if "description" in resource.keys():
                own["description"] = resource["description"]

            if "config" in resource.keys():
                own["config"] = resource["config"]
            elif "location" in resource.keys():
                own["location"] = resource["location"]
            elif "remote" in resource.keys():
                own["remote"] = resource["remote"]

            if "limit" in resource.keys():
                own["limit"] = resource["limit"]
            res[key] = own
        return res

    def store(self, rid: str, node: INode):
        entry = dict()
        temp = self.resources.get(rid)
        if temp:
            entry = temp

        meta = node.get_meta()
        if meta.get_name():
            entry["name"] = meta.get_name()

        if meta.get_description():
            entry["description"] = meta.get_description()

        entry["config"] = node.to_dict()
        self.resources.update({rid: entry})
        self.save()

    def save(self):
        print("[Registration] saves resources")
        with open(self.storefile, "w+") as f:
            json.dump(self.get_registered(["remote"]), f, indent=4)

    def remove(self, rid: str):
        if rid in self.resources.keys():
            self.resources.pop(rid)
            self.save()
            return True
        return False

    def load(self):
        # merge sources
        for source in self.sources:
            data = dict()
            try:
                f = urllib.request.urlopen(source)
                data = json.loads(f.read())
            except:
                path = Path(source)
                if not path.is_file():
                    print("[Registration] ignored: " + source)
                    continue
                with path.open("r") as f:
                    data = json.load(f)

            for key in data.keys():
                meta = data[key]
                resource = dict(name=key, description="")
                if "name" in meta.keys():
                    resource["name"] = meta["name"]

                if "description" in meta.keys():
                    resource["description"] = meta["description"]

                if "config" in meta.keys():
                    resource["config"] = meta["config"]
                elif "location" in meta.keys():
                    resource["location"] = meta["location"]
                elif "remote" in meta.keys():
                    resource["remote"] = meta["remote"]

                self.resources[key] = resource

        # merge entrypoints
        entrypoints = load_entrypoints("msys.modules")
        if entrypoints:
            for entry in entrypoints:
                try:
                    obj = entry.load()
                except:
                    continue

                meta = obj.to_dict()["meta"]

                resource = dict(name=entry.name, description="", location="uvicorn " + entry.value + " --port {port}",
                                limit=1)  # TODO: delete "limit=1" later

                if "name" in meta.keys():
                    resource["name"] = meta["name"]

                if "description" in meta.keys():
                    resource["description"] = meta["description"]

                self.resources[entry.name] = resource

        self.save()

    def __launch__(self, rid: str, resource: dict) -> "Processor":
        limit = False
        if "limit" in resource.keys():
            limit = resource["limit"]

        if "instances" not in resource.keys():
            resource["instances"] = []

        instances = resource["instances"]

        print("[Registration] __launch__: " + str(resource))

        if (limit is False) or (len(instances) < limit):
            # create new
            process = Processor(rid, resource["location"])
            instances.append(process)
        else:
            # return existing with least counts
            process = sorted(instances, key=lambda x: x.users)[0]
            process.start()
        return process

    def terminate_resource(self, process: "Processor"):
        # reduce counter
        process.stop()
        # delete if 0
        if process.users > 0:
            return
        rid = process.id
        if rid not in self.resources.keys():
            return None
        self.resources[rid]["instances"].remove(process)

    def launch(self, rid: str) -> "INode":
        resource = self.resources.get(rid)

        if not resource and rid:
            raise KeyError

        res = None
        if "location" in resource.keys() or "":
            process = self.__launch__(rid, resource)
            if not process:
                raise NotImplementedError
            from ..nodes import RemoteNode
            res = RemoteNode(process=process)

        # no rid or is module
        from ..nodes import Module
        res = Module(registration=self)

        if "config" in resource.keys():
            res.load(resource["config"])

        return res

    def __del__(self):
        self.save()
