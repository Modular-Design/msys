from pymsys import UUIDGenerator, ILink
from ..core import Registration
from typing import Optional


class RegisterGenerator(UUIDGenerator):
    def __init__(
            self,
            register: Registration,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.register = register

    def generate_class(self, key: Optional[str] = None) -> ILink:
        if key is None:
            return super().generate_class(key)
        return self.register.launch(key)
