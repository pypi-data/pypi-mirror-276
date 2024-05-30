from typing import Any, Type

class Collection:
    def __init__(self):
        self._items: dict[Type, Any] = {}
        self._byClassname: dict[str, Any] = {}

    @property
    def items(self) -> dict[Type, Any]:
        return self._items

    def __getitem__(self, key) -> Any:
        return self._items[key]

    def __setitem__(self, key, item: Any):
        self._items[key] = item

    @property
    def byClassname(self) -> dict[str, Any]:
        return self._byClassname

    @classmethod
    def getItemType(cls):
        return Any
