from random import Random
from typing import Optional, List


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


# MARKDOWN_DNA_TO_RNA
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
# MARKDOWN_DNA_TO_RNA


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