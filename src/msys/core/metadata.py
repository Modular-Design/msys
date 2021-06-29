from ..interfaces import ISerializer
from typing import Optional

class Point(ISerializer):
    def __init__(self,
                 x: Optional[float]=0.0,
                 y: Optional[float]=0.0):
        self.x = x
        self.y = y

    def load(self, json: dict) -> bool:
        if "x" in json.keys():
            self.x = json["x"]
        if "y" in json.keys():
            self.y = json["y"]
        return True

    def to_dict(self) -> dict:
        return self.__dict__


class Metadata(ISerializer):
    def __init__(self,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 color: Optional[str] = None,
                 pos: Optional[Point] = None,
                 inverted: Optional[bool] =False):
        self.name = name
        self.description = description
        self.color = color
        self.pos = pos
        self.inverted = inverted


    def load(self, json: dict) -> bool:
        if "name" in json.keys():
            self.name = json["name"]

        if "description" in json.keys():
            self.description = json["description"]

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
        if self.description:
            res.update({"description": self.description})
        return res
