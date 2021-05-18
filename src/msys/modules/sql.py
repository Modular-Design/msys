from ..core import Module
from ..core.connection import Input, Output


class SQL(Module):
    def __init__(self):
        super().__init__(inputs=[Input(), Input()], outputs=[Output()])