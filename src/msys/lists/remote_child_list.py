from pymsys import UpdatableChildList, ILink, IUpdatable, IGenerator
from typing import  Optional, Dict, Union


class RemoteChildList(UpdatableChildList):
    def __init__(self,
                 childs: Optional[Dict[str, Union[ILink, IUpdatable]]] = None,
                 key_generator: Optional[IGenerator] = None,
                 parent: Optional[ILink] = None,
                 ):
        super().__init__(childs=childs, key_generator=key_generator, parent=parent)
        self.processor = None
        self.init = True
        self.initiate()

    def set_parent(self, parent: ILink, key: Optional[str] = None) -> bool:
        from ..nodes import RemoteNode
        if not isinstance(parent, RemoteNode):
            raise TypeError
        super().set_parent(parent, key)
        self.processor = self.parent.get_processor()

    def initiate(self, config: Optional[dict] = None):
        if config:
            self.load(config)
        self.init = False

    def load(self, config: dict) -> bool:
        super().load(config)
        if not self.init:
            super().load(self.processor.change_config(self.parent.to_dict()))
