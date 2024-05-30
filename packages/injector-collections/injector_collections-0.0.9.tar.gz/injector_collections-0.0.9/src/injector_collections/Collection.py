from typing import Type

class Collection:
    def __init__(self):
        self._items: dict[Type, object] = {}
        self._byClassname: dict[str, object] = {}

    @property
    def items(self) -> dict[Type, object]:
        return self._items

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, item):
        self._items[key] = item

    @property
    def byClassname(self) -> dict[str, object]:
        return self._byClassname
