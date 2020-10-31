import typing
from collections import Counter
from itertools import permutations, accumulate
from typing import Tuple, List

with open('/home/user/Downloads/dataset_240281_6(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

spectrum = Counter([int(w) for w in data.strip().split()])
weights_table = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]


class HashableCounter(Counter):
    def __init__(self, v=None):
        super().__init__(v)
        self._cached_hash = None

    def __hash__(self):
        if self._cached_hash is None:
            self._cached_hash = hash(tuple(sorted(self.items())))
        return self._cached_hash


class HashableList(list):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)
        self._cached_hash = None

    def __hash__(self):
        if self._cached_hash is None:
            self._cached_hash = hash(tuple(self))
        return self._cached_hash


def is_consistent_with_spectrum(linear_peptide_theoretical_spectrum: typing.Counter[int]) -> bool:
    for k, v in linear_peptide_theoretical_spectrum.items():
        if spectrum[k] < v:
            return False
    return True


def cyclopeptide_spectrum(peptide: List[int]) -> typing.Counter[int]:
    prefix_masses = [0]
    for i, w in enumerate(peptide):
        prev_mass = prefix_masses[i]
        next_mass = prev_mass + w
        prefix_masses.append(next_mass)
    ret = [0]
    for k_end in range(0, len(prefix_masses)):
        for k_start in range(0, k_end):
            min_mass = prefix_masses[k_start]
            max_mass = prefix_masses[k_end]
            ret.append(max_mass - min_mass)
            if k_start > 0 and k_end < len(peptide):
                ret.append(prefix_masses[-1] - (prefix_masses[k_end] - prefix_masses[k_start]))
    return Counter(ret)


def linear_peptid_spectrum(peptide: List[int]) -> typing.Counter[int]:
    return Counter([0] + list(accumulate(peptide)))


candidate_peptides = {HashableList()}
final_peptides = set()
while len(candidate_peptides) > 0:
    # Branch
    new_candidate_peptides = set()
    for p in candidate_peptides:
        for w in weights_table:
            new_p = HashableList(p)
            new_p.append(w)
            new_candidate_peptides.add(new_p)
    candidate_peptides = new_candidate_peptides
    # Bound
    removal_set = set()
    for p in candidate_peptides:
        if sum(p) == max(spectrum.elements()):
            if cyclopeptide_spectrum(p) == spectrum:
                final_peptides.add(p)
            removal_set.add(p)
        elif not is_consistent_with_spectrum(linear_peptid_spectrum(p)):
            removal_set.add(p)
    candidate_peptides -= removal_set

ret = ' '.join(['-'.join([str(i) for i in p]) for p in final_peptides])
print(f'{ret}')