from msys.core.management.processor import Processor
from msys.core.helpers import load_entrypoints
import urllib
import json

class Registration():
    def __init__(self,
                 sources: Optional[str] = None):

        if sources is None:
            sources = []
        self.sources= sources
        self.resources = dict() # {"id","location", "limit":int, "instances" ["Process1", "Process2", etc.]}
        self.blueprints = dict() # {"id", "name", "description", "config" or "resource"}
        load_sources()

    def get_resources(self) -> dict:
        "use for printing"
        res = dict()
        for key in self.resources.keys():
            resource = self.resources[key]
            res[key] = dict(location=temp["location"])
        return res

    def get_blueprints(self) -> dict:
        "use for printing"
        return self.blueprints

    def load_sources(self):
        # merge sources
        for source in self.sources:
            try:
                f = urllib.request.urlopen(source)
                data = json.loads(f.read())
            except:
                data = dict()

            for key in data.keys():
                meta = data[key]
                source = dict(name=key, description="")
                if "name" in meta.keys():
                    source["name"] = meta["name"]

                if "description" in meta.keys():
                    source["description"] = meta["description"]

                if "config" in meta.keys():
                    source["config"] = meta["config"]

                if "resource" in meta.keys():
                    resource = meta["resource"]
                    if type(resource) == str:
                        source["resource"] = key
                    elif type(resource) == dict:
                        if "location" in resource.keys():
                            source["resource"] = key
                            self.resources[key] = resource
                        else:
                            source["resource"] = resource.keys()[0]
                            self.resources.update(resource)

                self.blueprints[key] = source

        # merge entrypoints
        entrypoints = load_entrypoints("msys.modules")
        if entrypoints:
            for entry in entrypoints:
                try:
                    obj = entry.load()
                except:
                    continue

                meta = obj.to_dict()["meta"]

                resource = dict(location="uvicorn " + entry.value + " --port {port}")
                source = dict(name=entry.name, description="", resource=entry.name)

                if "name" in meta.keys():
                    source["name"] = meta["name"]

                if "description" in meta.keys():
                    source["description"] = meta["description"]

                self.resources[entry.name] = resource
                self.blueprints[entry.name] = source


    def launch_resource(self, rid:str) -> "Processor":
        if rid not in self.resources.keys():
            return None

        resource = self.resources[rid]
        limit = False
        if "limit" in resource.keys():
            limit = resource["limit"]

        if "instances" not in resource.keys():
            resource["instances"] = []

        instances = resource["instances"]

        if (limit is False) or (len(instances) < limit):
            # create new
            process = Processor(rid, resource["location"])
            instances.append(process)
        else:
            # return existing with least counts
            process = sorted(instances, key=lambda x: x.users)[0]
            process.start()
        return process

    def terminate_resource(self, process:"Processor"):
        # reduce counter
        process.stop()
        # delete if 0
        if process.users > 0:
            return
        rid = process.id
        if rid not in self.resources.keys():
            return None
        self.resources[rid]["instances"].remove(process)
