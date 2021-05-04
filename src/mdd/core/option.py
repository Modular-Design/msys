from .serializer import SerializerInterface, includes
import uuid


class Option(SerializerInterface):
    def __init__(self, id=str(uuid.uuid4()), title="", default_value=[], description="", selection=[], single=True):
        self.id = id
        self.title = title
        self.description = description
        self.selection = selection
        self.single = single
        if default_value:
            self.value = default_value
        elif selection:
            self.value = [self.selection[0]]
        else:
            self.value = []

    def to_dict(self) -> dict:
        res = dict()
        if self.id:
            res.update({"id": self.id})
        if self.title:
            res.update({"title": self.title})
        if self.value:
            res.update({"value": self.value})
        if self.description:
            res.update({"description": self.description})
        if self.selection:
            res.update({"selection": self.selection, "single": self.single})

        return res

    def from_dict(self, json: dict) -> bool:
        if "id" in json.keys():
            self.id = json["id"]

        if "title" in json.keys():
            self.title = json["title"]

        value = None
        if "value" in json.keys():
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
        self.value = value
        return True