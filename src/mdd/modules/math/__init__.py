from ...core import Module
from ...core.connection import Input, Output
from ...core.option import Option
from ...core.optimisation import NumericStringParser
import numpy as np


class Math(Module):
    def __init__(self):
        self.__opt_expr = Option(id="eval",
                                 title="Evaluate:",
                                 description="""
                                        Enter mathematical Expression!
                                        The input value can be accessed by using the according input name.
                                        """,
                                 default_value="in0+in1")

        self.__opt_ins = Option(id="length",
                                title="Inputs:",
                                description="""
                                        Enter the number of inputs.
                                        Minimum: 0
                                        """,
                                default_value="2")

        super().__init__(inputs=[Input(), Input()],
                         outputs=[Output()],
                         options=[self.__opt_expr,
                                  self.__opt_ins,
                                  ])

        for i in range(len(self.inputs)):
            self.inputs[i].metadata.name = "in" + str(i)

    def process(self) -> None:
        parser = NumericStringParser()
        for i in range(len(self.inputs)):
            name = self.inputs[i].metadata.name
            parser.vars[name] = np.array(self.inputs[i].get_value())

        result = parser.eval(self.__opt_expr.value)
        if isinstance(result, np.ndarray):
            self.outputs[0].set_value(list(result))
        else:
            self.outputs[0].set_value([result])
