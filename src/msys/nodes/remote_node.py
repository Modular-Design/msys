from ..core import Processor
from typing import Optional
from ..lists import RemoteChildList
from pymsys import Node, Option, ILink, IMetadata, Generator, Connectable


class RemoteNode(Node):
    def __init__(
            self,
            process: Processor,
            meta: Optional[IMetadata] = None,
            ram_reserve: Optional[float] = 0.0,
            parent: Optional[ILink] = None,
    ):
        super().__init__(
            meta=meta,
            input_generator=Generator(default_class=Connectable),
            output_generator=Generator(default_class=Connectable),
            option_generator=Generator(default_class=Option),
            input_list=RemoteChildList,
            output_list=RemoteChildList,
            option_list=RemoteChildList,
            ram_reserve=ram_reserve,
            parent=parent,
            url="LATER",  # TODO: add later
        )

        self.process = process
        self.load(self.process.get_config())

    def get_processor(self) -> Processor:
        return self.process

    def process(self, input_changed: bool):
        if input_changed:
            self.load(self.process.update_config(self.to_dict()))
