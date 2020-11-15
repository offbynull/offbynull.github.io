from typing import List, FrozenSet, Dict, Tuple

from Utils import T


def rotate(peptide: List[T]):
    ret = []
    for i in range(0, len(peptide)):
        rotated = peptide[i:] + peptide[:i]
        ret.append(rotated)
    return ret


def count_rotation_occurrences(peptides: List[List[T]]) -> Tuple[List[T], int]:
    potential_cyclic_peptides: Dict[FrozenSet[T], List[List[T]]] = dict()
    for peptide in peptides:
        aa_set = frozenset(peptide)
        aa_set_peptides = potential_cyclic_peptides.setdefault(aa_set, [])
        aa_set_peptides.append(peptide)
    ret = []
    for aa_set, aa_set_peptides in potential_cyclic_peptides.items():
        for peptide in aa_set_peptides:
            peptide_rotated_versions = rotate(peptide)
            count = sum([aa_set_peptides.count(p) for p in peptide_rotated_versions])
            ret.append((peptide, count))
    return ret


if __name__ == '__main__':
    print(f'{count_rotation_occurrences([[1, 2, 3, 4], [0, 1, 0], [3, 4, 1, 2], [1, 0, 0]])}')