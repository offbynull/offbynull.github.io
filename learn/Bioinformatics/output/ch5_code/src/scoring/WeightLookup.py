from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Tuple, Dict

ELEM = TypeVar('ELEM')


class WeightLookup(ABC):
    @abstractmethod
    def lookup(self, *elements: Tuple[Optional[ELEM], ...]):
        ...


class ConstantWeightLookup(WeightLookup):
    def __init__(self, match_weight: float, mismatch_weight: float, indel_weight: float):
        self.match_weight = match_weight
        self.misatch_weight = mismatch_weight
        self.indel_weight = indel_weight

    def lookup(self, *elements: Tuple[Optional[ELEM], ...]):
        if None in elements:
            return self.indel_weight
        return self.match_weight if len(set(elements)) == 1 else self.misatch_weight


class TableWeightLookup(WeightLookup):
    def __init__(self, weight_lookup: Dict[Tuple[ELEM, ...], float], indel_weight: float):
        self.weight_lookup = weight_lookup
        self.indel_weight = indel_weight

    @staticmethod
    def create_from_2d_matrix_file(weight_lookup_path: str, indel_weight: float):
        with open(weight_lookup_path, mode='r', encoding='utf-8') as f:
            data = f.read()
        return TableWeightLookup.create_from_2d_matrix_str(data, indel_weight)

    @staticmethod
    def create_from_2d_matrix_str(data: str, indel_weight: float):
        weight_lookup = {}
        lines = data.strip().split('\n')
        aa_row = lines[0].strip().split()
        for line in lines[1:]:
            vals = line.strip().split()
            aa2 = vals[0]
            weight = vals[1:]
            for aa1, weight in zip(aa_row, weight):
                weight_lookup[(aa1, aa2)] = float(weight)
        return TableWeightLookup(weight_lookup, indel_weight)

    def lookup(self, *elements: Tuple[Optional[ELEM], ...]):
        if None in elements:
            return self.indel_weight
        return self.weight_lookup[elements]


if __name__ == '__main__':
    x = TableWeightLookup.create_from_2d_matrix_file('../PAM250.txt', -5.0)
    print(f'{x.lookup("S", "A")}')
    print(f'{x.lookup("S", None)}')
    print(f'{x.lookup(None, "A")}')
