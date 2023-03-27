import collections
from typing import Any


class DictWithIndex(collections.abc.Mapping):
    def __init__(self, items: list[Any] = None):
        self._items = {}
        self.global_list = []

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        self._items[key] = value
        if len(value) > 0:
            self.global_list.append(value[-1])

    def __delitem__(self, key):
        del self._items[key]

    def __len__(self):
        return len(self._items)

    def __contains__(self, key):
        return key in self._items

    def get_global_list(self):
        return self.global_list
