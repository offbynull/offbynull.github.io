from __future__ import annotations

from itertools import product
from typing import Iterator, TypeVar, Generic

ID = TypeVar('ID')


class SimilarityMatrix(Generic[ID]):
    def __init__(self, initial: dict[tuple[ID, ID], float]):
        d = {}
        ids = {id for id_pair in initial.keys() for id in id_pair}
        for id1, id2 in product(ids, repeat=2):
            opt1 = (id1, id2) in initial
            opt2 = (id2, id1) in initial
            if opt1 and opt2 and initial[(id1, id2)] != initial[(id2, id1)]:
                raise ValueError(f'Similarity between leaf nodes inserted twice but distances are not the same: {(id1, id2)} / {(id2, id1)}')
            if opt1:
                dist = initial[(id1, id2)]
            elif opt2:
                dist = initial[(id2, id1)]
            else:
                raise ValueError(f'Expected similarity for {(id1, id2)}')
            id1, id2 = sorted([id1, id2])
            d[(id1, id2)] = dist
        self._data = d
        self._keys = ids

    def delete(self, id: ID):
        if id not in self._keys:
            raise ValueError(f'{id} does not already exists')
        dels = []
        for i1, i2 in self._data.keys():
            if i1 == id or i2 == id:
                dels.append((i1, i2))
        for key in dels:
            del self._data[key]
        self._keys.remove(id)

    def insert(self, new_id: ID, similarities: dict[ID, float]) -> None:
        if new_id in self._keys:
            raise ValueError(f'{new_id} already exists')
        if new_id not in similarities:
            raise ValueError(f'{new_id} similarity to self missing')
        for k in self._keys:
            if k not in similarities:
                raise ValueError(f'{k} missing')
        for other_id in self._keys:
            i1, i2 = sorted((new_id, other_id))
            self._data[(i1, i2)] = similarities[other_id]
        self._keys.add(new_id)

    def merge(self, new_id: ID, old_id1: ID, old_id2: ID, distances: dict[ID, float]) -> None:
        self.delete(old_id1)
        self.delete(old_id2)
        return self.insert(new_id, distances)

    def leaf_ids(self) -> set[ID]:
        return self._keys.copy()

    def leaf_ids_it(self) -> Iterator[ID]:
        return iter(self._keys)

    def copy(self) -> SimilarityMatrix:
        return SimilarityMatrix(self._data)

    @property
    def n(self):
        return len(self._keys)

    def __getitem__(self, key: tuple[ID, ID]) -> float:
        i1, i2 = sorted(key)
        return self._data[(i1, i2)]

    def __setitem__(self, key: tuple[ID, ID], value: float):
        i1, i2 = sorted(key)
        self._data[(i1, i2)] = value

    def __str__(self) -> str:
        ret = '       '
        for i1 in sorted(self._keys):
            ret += f'{i1}'.ljust(7, ' ')
        ret += '\n'
        for i1 in sorted(self._keys):
            ret += f'{i1}'.ljust(7, ' ')
            for i2 in sorted(self._keys):
                entry = tuple(sorted((i1, i2)))
                ret += f'{self[entry]}'.ljust(7, ' ')
            ret += '\n'
        return ret[:-1]

    @staticmethod
    def create_from_matrix(m: list[list[float]]) -> SimilarityMatrix:
        d = {}
        for i in range(len(m)):
            for j in range(len(m)):
                i1, i2 = sorted([i, j])
                d[(i1, i2)] = float(m[i1][i2])
        return SimilarityMatrix(d)
