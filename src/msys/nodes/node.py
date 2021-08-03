from src.msys.core.processor import Processor

from src.msys.interfaces import INode
from src.msys.core.child import Child, IChild
from typing import Optional, List, Dict
from src.msys.core.connectable import Connectable
from pymsys.nodes import Node
from pymsys.interfaces import ILink, IMetadata, IGenerator


class Node(Node):
    def __init__(self,
                 parent: Optional[ILink] = None,
                 meta: Optional[IMetadata] = None,
                 inputs: Optional[Dict[str, Connectable]] = None,
                 outputs: Optional[Dict[str, Connectable]] = None,
                 options: Optional[Dict[str, Option]] = None,
                 input_generator: Optional[IGenerator] = False,
                 output_generator: Optional[IGenerator] = False,
                 option_generator: Optional[IGenerator] = None,
                 ram_reserve: Optional[float] = 0.0, ):

        super().__init__(parent,
                         meta,
                         inputs,
                         outputs,
                         options,
                         input_generator,
                         output_generator,
                         option_generator,
                         ram_reserve)

    def update(self) -> bool:
        for inp in self.inputs:
            if inp.update():
                pass

        self.load(self.process.update_config(self.to_dict()))

        for out in self.outputs:
            if out.update():
                pass

    def is_changed(self) -> bool:
        for inp in self.inputs:
            if inp.is_changed():
                return True

        for out in self.outputs:
            if out.is_changed():
                return True

    def exit(self):
        del self
        # if self.process is not None:
        #    self.process.kill()
        pass
