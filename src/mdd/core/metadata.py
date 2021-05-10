from .serializer import SerializerInterface, includes


class Point(SerializerInterface):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def from_dict(self, json: dict) -> bool:
        if "x" in json.keys():
            self.x = json["x"]
        if "y" in json.keys():
            self.y = json["y"]
        return True

    def to_dict(self) -> dict:
        return self.__dict__


class Metadata(SerializerInterface):
    def __init__(self, name="", color="", pos=None, inverted=False):
        self.name = name
        self.color = color
        self.pos = pos
        self.inverted = inverted

    def from_dict(self, json: dict) -> bool:
        if "name" in json.keys():
            self.name = json["name"]

        if "color" in json.keys():
            self.color = json["color"]

        if "pos" in json.keys():
            if not self.pos:
                self.pos = Point()
            self.pos.from_dict(json["pos"])

        if "inverted" in json.keys():
            self.inverted = json["inverted"]

        return True

    def to_dict(self) -> dict:
        res = dict()
        if self.name:
            res.update({"name": self.name})
        if self.color:
            res.update({"color": self.color})
        if self.pos:
            res.update({"pos": self.pos.to_dict()})
        if self.inverted:
            res.update({"inverted": self.inverted})
        return res
