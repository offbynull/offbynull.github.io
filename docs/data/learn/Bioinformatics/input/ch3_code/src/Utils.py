from __future__ import annotations

from random import Random
from typing import Tuple, Optional, List

from Kdmer import Kdmer


def count_kmers(data_len: int, k: int) -> int:
    return data_len - k + 1


def slide_window(data: str, k: int) -> Tuple[str, int]:
    for i in range(0, len(data) - k + 1):
        yield data[i:i+k], i


def slide_window_kd(data: str, k: int, d: int) -> Tuple[Kdmer, int]:
    for a, b in zip(slide_window(data, k), slide_window(data[k+d:], k)):
        yield Kdmer(a[0], b[0], d), a[1]


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
