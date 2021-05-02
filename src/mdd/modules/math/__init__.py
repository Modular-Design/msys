from ...core import Module
from ...core.connection import Input, Output
from ...core.option import Option


class Math(Module):
    def __init__(self):
        super().__init__(inputs=[Input(), Input()],
                         outputs=[Output()],
                         options=[Option(title="Method:",
                                         description="Select a Method!",
                                         selection=["add", "substract", "multiply", "divide", "custom"])])