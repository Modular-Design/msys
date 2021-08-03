from ..core import Processor, Connectable
from typing import Optional, Dict

from pymsys import Node, Option
from pymsys.interfaces import ILink, IMetadata, IGenerator


class RemoteNode(Node):
    def __init__(self,
                 process: Processor,
                 parent: Optional[ILink] = None,
                 meta: Optional[IMetadata] = None,
                 inputs: Optional[Dict[str, Connectable]] = None,
                 outputs: Optional[Dict[str, Connectable]] = None,
                 options: Optional[Dict[str, Option]] = None,
                 input_generator: Optional[IGenerator] = False,
                 output_generator: Optional[IGenerator] = False,
                 option_generator: Optional[IGenerator] = None,
                 ram_reserve: Optional[float] = 0.0,):

        super().__init__(parent,
                         meta,
                         inputs,
                         outputs,
                         options,
                         input_generator,
                         output_generator,
                         option_generator,
                         ram_reserve)

        self.process = process
        self.load(self.process.get_config())

    def get_processor(self) -> Processor:
        return self.process

    def update(self) -> bool:
        for inp in self.inputs:
            if inp.update():
                pass

        self.load(self.process.update_config(self.to_dict()))

        for out in self.outputs:
            if out.update():
                pass

