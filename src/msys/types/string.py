from ..core.type import Type

class StringType(StandardType):
    def __init__(self, default_value=""):
        super().__init__(type_name="string", default_value=default_value)
