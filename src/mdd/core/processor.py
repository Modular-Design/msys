from .module import Module


class Processor(Module):
    def __init__(self, inputs=[], outputs=[], options=[], modules=[]):
        super().__init__(inputs=inputs, outputs=outputs, options=options)
        self.modules = modules


    def get_childs(self) -> []:
        return self.inputs + self.outputs + self.modules
