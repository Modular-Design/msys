from .interfaces import SerializerInterface

class Registrable(SerializerInterface):
    def __init__(self):
        self.registered_name = ""
        self.registered_package = ""

    def to_dict(self) -> dict:
        res = dict()
        if self.registered_name:
            res["name"] = self.registered_name

        if self.registered_package:
            res["package"] = self.registered_package

        if res:
            return {"registered": res}
        else:
            return {}

    def from_dict(self, json: dict) -> bool:
        if "registered" in json.keys():
            res = json["registered"]
            if "name" in res.keys():
                 self.registered_name = res["name"]

            if "package" in res.keys():
                 self.registered_package = res["package"]
            return True

        return False
