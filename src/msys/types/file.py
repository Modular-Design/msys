import pathlib

from ..core.type import StandardType


class FileType(StandardType):
    def __init__(self, name="", value=b""):
        self.file_name = name
        super().__init__(default_value=value)

    def from_dict(self, json: dict) -> bool:
        if not "file_name" in json.keys():
            return False
        self.file_name = json["file_name"]
        return super().from_dict(json)

    def to_dict(self) -> dict:
        res = super().to_dict()
        res["file_name"] = self.file_name
        return res

    @staticmethod
    def from_path(path):
        p = pathlib.Path(path)
        try:
            return FileType(p.name, p.read_bytes())
        except FileNotFoundError:
            print(f"File {path} could not be read")
