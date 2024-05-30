from typing import Type
from injector_collections.CollectionItem import CollectionItem

class Collection:
    def __init__(self):
        self._items: dict[Type[CollectionItem], CollectionItem] = {}
        self._byClassname: dict[str, CollectionItem] = {}

    @property
    def items(self) -> dict[Type[CollectionItem], CollectionItem]:
        return self._items

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, item):
        self._items[key] = item

    @property
    def byClassname(self) -> dict[str, CollectionItem]:
        return self._byClassname
