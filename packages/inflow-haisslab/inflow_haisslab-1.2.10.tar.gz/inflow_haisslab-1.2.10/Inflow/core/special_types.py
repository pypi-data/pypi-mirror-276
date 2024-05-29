# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 15:57:47 2023

@author: tjostmou
"""


def make_hashable(dataframe):
    def to_hashable(cell):
        if isinstance(cell, list):
            return HashableList(cell)
        if isinstance(cell, dict):
            return HashableDict(cell)
        if isinstance(cell, set):
            return HashableSet(cell)
        return cell

    return dataframe.applymap(to_hashable)


class AttrDict(dict):
    # a class to make dictionnary keys accessible with attribute syntax
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class IndexableList(list):  # a list you can get a subsection of as you would do with a pd dataframe or series
    # it expects a BOOLEAN index mask that matches the length of the list
    def __init__(self, iterable):
        super().__init__(iterable)

    def __getitem__(self, index):
        import pandas as pd, numpy as np

        if isinstance(index, (list, np.ndarray, pd.core.series.Series)) and len(index) == len(self):
            return IndexableList([item for item, selected in zip(self, index) if selected])
        return super().__getitem__(index)


class HashableList(list):
    def __init__(self, alist):
        content = []
        for item in alist:
            if isinstance(item, list):
                item = HashableList(item)
            elif isinstance(item, dict):
                item = HashableDict(item)
            elif isinstance(item, set):
                item = HashableSet(item)
            content.append(item)
        super().__init__(content)

    def __hash__(self):
        return hash(tuple(sorted(self, key=lambda item: item.__hash__())))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __gt__(self, other):
        return self.__hash__() > other.__hash__()


class HashableDict(dict):
    def __init__(self, adict):
        content = {}
        for key, value in adict.items():
            if isinstance(value, dict):
                value = HashableDict(value)
            elif isinstance(value, list):
                value = HashableList(value)
            elif isinstance(value, set):
                value = HashableSet(value)
            content[key] = value
        super().__init__(content)

    def __hash__(self):
        return hash(frozenset(sorted(self.items(), key=lambda item: item[1].__hash__())))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __gt__(self, other):
        return self.__hash__() > other.__hash__()


class HashableSet(set):
    def __init__(self, aset):
        content = set()
        for item in aset:
            if isinstance(item, dict):
                item = HashableDict(item)
            elif isinstance(item, list):
                item = HashableList(item)
            elif isinstance(item, set):
                item = HashableSet(item)
            content.add(item)
        super().__init__(content)

    def __hash__(self):
        return hash(frozenset(self))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __gt__(self, other):
        return self.__hash__() > other.__hash__()
