from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Tuple, Dict

ELEM = TypeVar('ELEM')


class WeightLookup(ABC):
    @abstractmethod
    def lookup(self, *elements: Tuple[Optional[ELEM]]):
        ...



class Constant2DWeightLookup(WeightLookup):
    def __init__(self, match_weight: int, mismatch_weight: int, indel_weight: int):
        self.match_weight = match_weight
        self.misatch_weight = mismatch_weight
        self.indel_weight = indel_weight

    def lookup(self, *elements: Tuple[Optional[ELEM]]):
        if elements[0] is None or elements[1] is None:
            return self.indel_weight
        return self.match_weight if elements[0] == elements[1] else self.misatch_weight


class Table2DWeightLookup(WeightLookup):
    def __init__(self, weight_lookup: Dict[Tuple[ELEM, ELEM], int], indel_weight: int):
        self.weight_lookup = weight_lookup
        self.indel_weight = indel_weight

    @staticmethod
    def create_from_file(weight_lookup_path: str, indel_weight: int):
        weight_lookup = {}
        with open(weight_lookup_path, mode='r', encoding='utf-8') as f:
            data = f.read()
        lines = data.strip().split('\n')
        aa_row = lines[0].strip().split()
        for line in lines[1:]:
            vals = line.strip().split()
            aa2 = vals[0]
            weight = vals[1:]
            for aa1, weight in zip(aa_row, weight):
                weight_lookup[(aa1, aa2)] = int(weight)
        return Table2DWeightLookup(weight_lookup, indel_weight)

    def lookup(self, *elements: Tuple[Optional[ELEM]]):
        if elements[0] is None or elements[1] is None:
            return self.indel_weight
        return self.weight_lookup[elements]


if __name__ == '__main__':
    x = Table2DWeightLookup.create_from_file('PAM250.txt', -5)
    print(f'{x.lookup("S", "A")}')
    print(f'{x.lookup("S", None)}')
    print(f'{x.lookup(None, "A")}')
