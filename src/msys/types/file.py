import pathlib

from ..core.type import StandardType


class FileType(StandardType):
    def __init__(self, name="", value=b""):
        self.file_name = name
        super().__init__(default_value=value)

    def from_dict(self, json: dict) -> bool:
        if "file_name" in json.keys():
            self.file_name = json["file_name"]
        return super().from_dict(json)

    def to_dict(self) -> dict:
        res = super().to_dict()
        if self.file_name:
            res["file_name"] = self.file_name
        return res

    @classmethod
    def from_path(cls, path):
        p = pathlib.Path(path)
        return FileType(p.name, p.read_bytes())
