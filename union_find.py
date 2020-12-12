import numpy as np


class UnionFind:

    def __init__(self, elements: int):
        self._elements = elements
        self._parents = np.zeros(shape=(elements,), dtype='int32')
        self._ranks = np.zeros(shape=(elements,), dtype='int32')
        for i in range(elements):
            self._parents[i] = i
    
    @property
    def parents(self):
        return self._parents

    def compress_paths(self):
        for i in range(self._elements):
            self.find(i)

    def find(self, element: int):
        if self._parents[element] == element:
            return element
        
        # Path compression
        self._parents[element] = self.find(self._parents[element])
        return self._parents[element]

    def union(self, first: int, second: int):
        fParent = self.find(first)
        sParent = self.find(second)

        if fParent == sParent:
            return

        maxRank = fParent if self._ranks[fParent] >= self._ranks[sParent] else sParent
        minRank = fParent if self._ranks[fParent] < self._ranks[sParent] else sParent

        self._parents[minRank] = maxRank
        # Rankins is used and increased every time the height of the tree changes
        if self._ranks[maxRank] == self._ranks[minRank]:
            self._ranks[maxRank] += 1
