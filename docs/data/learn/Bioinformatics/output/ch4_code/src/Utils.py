from __future__ import annotations

from random import Random
from typing import Tuple, Optional, List, TypeVar


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
    'UAA': '',
    'UAC': 'Y',
    'UAG': '',
    'UAU': 'Y',
    'UCA': 'S',
    'UCC': 'S',
    'UCG': 'S',
    'UCU': 'S',
    'UGA': '',
    'UGC': 'C',
    'UGG': 'W',
    'UGU': 'C',
    'UUA': 'L',
    'UUC': 'F',
    'UUG': 'L',
    'UUU': 'F'
}

def codon_to_amino_acid(rna: str) -> Optional[str]:
    return _codon_to_amino_acid.get(rna)


_amino_acid_to_codons = dict()
for k, v in _codon_to_amino_acid.items():
    _amino_acid_to_codons.setdefault(v, []).append(k)

def amino_acid_to_codons(codon: str) -> Optional[List[str]]:
    return _amino_acid_to_codons.get(codon)