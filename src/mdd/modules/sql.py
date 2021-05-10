from mdd.core import Module
from mdd.core.connection import Input, Output


class SQL(Module):
    def __init__(self):
        super().__init__(inputs=[Input(), Input()], outputs=[Output()])