from __future__ import annotations

from typing import Tuple, List, TypeVar, Generator


S = TypeVar('S', str, List)


def count_kmers(data_len: int, k: int) -> int:
    return data_len - k + 1


# This method checks to make sure that all elements of sorted_this are contained in sorted_other. Both lists must be
# sorted smallest to largest.
def contains_all_sorted(sorted_this: S, sorted_other: S) -> bool:
    this_idx = 0
    other_idx = 0
    for i in range(0, len(sorted_this)):
        this_elem = sorted_this[this_idx]
        if other_idx >= len(sorted_other):
            return False
        other_elem = sorted_other[other_idx]
        while other_elem < this_elem:
            other_idx += 1
            other_elem = sorted_other[other_idx]
        if other_elem > this_elem:
            return False
        this_idx += 1
        other_idx += 1
    return True


def rotate_right(l: S) -> Generator[S]:
    for i in range(0, len(l)):
        yield l[i:] + l[:i]


def rotate_left(l: S) -> Generator[S]:
    for i in range(len(l), -1, -1):
        yield l[i:] + l[:i]


def slide_window(data: S, k: int, cyclic: bool = False) -> Tuple[S, int]:
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


def enumerate_patterns(k: int, elements: S) -> Generator[S]:
    def inner(current: str, k: int, elements: S):
        if k == 0:
            yield current
        else:
            for element in elements:
                yield from inner(current + element, k - 1, elements)

    yield from inner('', k, elements)