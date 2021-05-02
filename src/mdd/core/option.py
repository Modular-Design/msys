from .serializer import SerializerInterface, includes


class Option(SerializerInterface):
    def __init__(self, title="", default_value=[], description="", selection=[], single=True):
        self.title = title
        self.description = description
        self.selection = selection
        self.single = single
        if default_value:
            self.value = default_value
        elif selection:
            self.value = [self.selection[0]]
        else:
            self.value = [""]

    def toDict(self) -> dict:
        res = dict(title=self.title, value=self.value)
        if self.description:
            res.update({"description": self.description})
        if self.selection:
            res.update({"selection": self.selection, "single": self.single})

        return res

    def fromDict(self, json: dict) -> bool:
        if not includes(json.keys(), ["title", "value"]):
            return False

        self.title = json["title"]
        value = json["value"]

        if "description" in json.keys():
            self.description = json["description"]

        if includes(json.keys(), ["selection", "single"]):
            self.selection = json["selection"]
            self.single = json["single"]
            if not includes(self.selection, value):
                return False

        if len(value) != 1 and self.single:
            return False
        self.value = json["value"]
        return True