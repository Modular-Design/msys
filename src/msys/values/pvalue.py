from pymsys.values import Value
from typing import Optional


class RemoteValue(Value):
    def __init__(self, default_value: Optional[dict] = None):
        super().__init__(default_value)
        self.processor = None
        self.node = None
        self.init = True

    def is_allowed(self, config: dict) -> bool:
        if self.processor is None or self.node is None:
            child_list = self.connectable.get_parent()
            if child_list is None:
                raise ValueError
            node = child_list.get_parent()
            if node is None:
                raise ValueError

            from ..nodes import RemoteNode
            if not isinstance(node, RemoteNode):
                raise TypeError
            self.node = node
            self.processor = node.get_processor()

        if self.init:
            self.init = False
            return True

        fallback = self.value
        self.value = config
        result = False
        if self.processor.change_config(self.node.to_dict()):
            result = True

        self.value = fallback
        return result
