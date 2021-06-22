from .serializer import SerializerInterface


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

    def from_dict(self, json: dict, safe=False) -> bool:
        if "registered" in json.keys():
            res = json["registered"]
            if "name" in res.keys():
                 self.registered_name = res["name"]

            if "package" in res.keys():
                 self.registered_package = res["package"]
            return True

        return False




def get_class_info(rclass):
    import re
    patern = r"<class '(.*?)'>"
    string = str(rclass)
    id, = re.findall(patern, string)
    res = id.split(".")
    if len(res) > 1:
        return dict(package=res[0], name=res[-1])
    else:
        return dict(package=[], name=res[0])


def set_class_info(rclass, info) -> bool:
    if not issubclass(rclass, Registrable):
        return False
    rclass.registered_name = info["name"]
    rclass.registered_package = info["package"]
    return True