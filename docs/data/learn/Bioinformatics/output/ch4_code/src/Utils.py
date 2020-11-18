from __future__ import annotations

from collections import Counter
from random import Random
from typing import Tuple, Optional, List, TypeVar, Dict, Generator


def count_kmers(data_len: int, k: int) -> int:
    return data_len - k + 1


def slide_window(data: str, k: int, cyclic: bool = False) -> Tuple[str, int]:
    for i in range(0, len(data) - k + 1):
        yield data[i:i+k], i
    if not cyclic:
        return
    for i in range(len(data) - k + 1, len(data)):
        rem = k - (len(data) - i)
        yield data[i:] + data[:rem], i


def split_to_size(data: str, n: int) -> List[str]:
    i = 0
    while i < len(data):
        end_i = min(len(data), i + n)
        yield data[i:end_i]
        i += n


def enumerate_patterns(k: int, elements='ACGT') -> str:
    def inner(current: str, k: int, elements: str):
        if k == 0:
            yield current
        else:
            for element in elements:
                yield from inner(current + element, k - 1, elements)

    yield from inner('', k, elements)


def generate_random_genome(size: int, r: Optional[Random] = None) -> str:
    if r is None:
        r = Random()
    return ''.join([r.choice(['A', 'C', 'T', 'G']) for i in range(size)])


def generate_random_cyclic_genome(size: int, copies: int, r: Optional[Random] = None) -> List[str]:
    if r is None:
        r = Random()
    copies = [''.join([r.choice(['A', 'C', 'T', 'G']) for i in range(size)])] * copies
    for i, copy in enumerate(copies):
        offset = r.randint(0, size)
        copies[i] = copy[offset+1:] + copy[:offset]
    return copies





def dna_reverse_complement(dna: str):
    return dna_complement(dna)[::-1]


def dna_complement(dna: str):
    ret = ''
    for ch in dna:
        if ch == 'A':
            ret += 'T'
        elif ch == 'C':
            ret += 'G'
        elif ch == 'T':
            ret += 'A'
        elif ch == 'G':
            ret += 'C'
        else:
            raise
    return ret


def dna_to_rna(dna: str):
    ret = ''
    for ch in dna:
        if ch == 'A' or ch == 'C' or ch == 'G':
            ret += ch
        elif ch == 'T':
            ret += 'U'
        else:
            raise
    return ret


def rna_to_dna(rna: str):
    ret = ''
    for ch in rna:
        if ch == 'A' or ch == 'C' or ch == 'G':
            ret += ch
        elif ch == 'U':
            ret += 'T'
        else:
            raise
    return ret


_codon_to_amino_acid = {
    'AAA': 'K',
    'AAC': 'N',
    'AAG': 'K',
    'AAU': 'N',
    'ACA': 'T',
    'ACC': 'T',
    'ACG': 'T',
    'ACU': 'T',
    'AGA': 'R',
    'AGC': 'S',
    'AGG': 'R',
    'AGU': 'S',
    'AUA': 'I',
    'AUC': 'I',
    'AUG': 'M',
    'AUU': 'I',
    'CAA': 'Q',
    'CAC': 'H',
    'CAG': 'Q',
    'CAU': 'H',
    'CCA': 'P',
    'CCC': 'P',
    'CCG': 'P',
    'CCU': 'P',
    'CGA': 'R',
    'CGC': 'R',
    'CGG': 'R',
    'CGU': 'R',
    'CUA': 'L',
    'CUC': 'L',
    'CUG': 'L',
    'CUU': 'L',
    'GAA': 'E',
    'GAC': 'D',
    'GAG': 'E',
    'GAU': 'D',
    'GCA': 'A',
    'GCC': 'A',
    'GCG': 'A',
    'GCU': 'A',
    'GGA': 'G',
    'GGC': 'G',
    'GGG': 'G',
    'GGU': 'G',
    'GUA': 'V',
    'GUC': 'V',
    'GUG': 'V',
    'GUU': 'V',
    'UAA': '*',
    'UAC': 'Y',
    'UAG': '*',
    'UAU': 'Y',
    'UCA': 'S',
    'UCC': 'S',
    'UCG': 'S',
    'UCU': 'S',
    'UGA': '*',
    'UGC': 'C',
    'UGG': 'W',
    'UGU': 'C',
    'UUA': 'L',
    'UUC': 'F',
    'UUG': 'L',
    'UUU': 'F'
}

_amino_acid_to_codons = dict()
for k, v in _codon_to_amino_acid.items():
    _amino_acid_to_codons.setdefault(v, []).append(k)


def codon_to_amino_acid(rna: str) -> Optional[str]:
    return _codon_to_amino_acid.get(rna)


def amino_acid_to_codons(codon: str) -> Optional[List[str]]:
    return _amino_acid_to_codons.get(codon)


def get_codon_to_amino_acid_table() -> Dict[str, str]:
    return _codon_to_amino_acid.copy()


def get_amino_acid_to_codons_table() -> Dict[str, List[str]]:
    return _amino_acid_to_codons.copy()


_amino_acid_to_mass = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113,
                       'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156,
                       'Y': 163, 'W': 186}

_mass_to_amino_acids = dict()
for k, v in _amino_acid_to_mass.items():
    _mass_to_amino_acids.setdefault(v, []).append(k)


def get_amino_acid_to_mass_table() -> Dict[str, int]:
    return _amino_acid_to_mass.copy()


def get_mass_to_amino_acids_table() -> Dict[int, List[str]]:
    return _mass_to_amino_acids.copy()


_unique_amino_acid_masses_as_dict = dict([(m, m) for m in _amino_acid_to_mass.values()])


# intended to be used as a replacement for get_amino_acid_to_mass_table(), because for certain problems we only track
# the masses, not what the actual amino acid was.
def get_unique_amino_acid_masses_as_dict() -> Dict[int, int]:
    return _unique_amino_acid_masses_as_dict.copy()


def mass_sequence_to_amino_acid_sequence_possibilities(mass_chain: List[int]) -> List[List[str]]:
    ret = [[]]
    for m in mass_chain:
        aas = _mass_to_amino_acids[m]
        new_ret = []
        for r in ret:
            for aa in aas:
                r = r.copy()
                r.append(aa)
                new_ret.append(r)
        ret = new_ret
    return ret


class HashableCounter(Counter):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class HashableList(list):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(self))


class HashableSet(set):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(self))


class HashableDict(dict):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


N = TypeVar('N', int, float)
T = TypeVar('T')


# This method checks to make sure that all elements of sorted_this are contained in sorted_other. Both lists must be
# sorted smallest to largest.
def contains_all_sorted(sorted_this: List[T], sorted_other: List[T]) -> bool:
    this_idx = 0
    other_idx = 0
    for i in range(0, len(sorted_this)):
        this_elem = sorted_this[this_idx]
        other_elem = sorted_other[other_idx]
        while other_elem < this_elem:
            other_idx += 1
            other_elem = sorted_other[other_idx]
        if other_elem > this_elem:
            return False
        this_idx += 1
        other_idx += 1
    return True


def rotate(l: List[T]) -> Generator[T]:
    for i in range(0, len(l)):
        yield l[i:] + l[:i]
