from __future__ import annotations

from math import ceil
from typing import TypeVar


class StringView:
    __slots__ = ('start', 'stop', 'data')

    @staticmethod
    def wrap(data: str) -> StringView:
        return StringView(0, len(data), data)

    def __init__(self, start: int, stop: int, data: str):
        self.start = start
        self.stop = stop
        self.data = data

    def __len__(self):
        return self.stop - self.start

    def __getitem__(self, item):
        if isinstance(item, slice):
            if item.step is not None and item.step > 1:
                raise ValueError('Only step size of 1 allowed')
            # start
            if item.start is None:
                new_start = self.start
            elif item.start < 0:
                new_start = self.stop + item.start
            else:
                new_start = self.start + item.start
            # stop
            if item.stop is None:
                new_stop = self.stop
            elif item.stop < 0:
                new_stop = self.stop + item.stop
            else:
                new_stop = self.start + item.stop
            # oob check
            if new_start < self.start or new_start > self.stop\
                    or new_stop < self.start or new_stop > self.stop:
                raise ValueError('Out of bounds')
            # return
            return StringView(new_start, new_stop, self.data)
        elif isinstance(item, int):
            if item < 0:
                return self.data[self.stop + item]
            else:
                return self.data[self.start + item]
        else:
            raise ValueError('Only slicing allowed')

    def __contains__(self, key: str):
        if len(key) == 0:
            return True
        elif len(key) > 1:
            raise ValueError('Single character values only')
        return any(ch == key for i, ch in enumerate(self))

    def __str__(self):
        return self.data[self.start:self.stop]

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return (self.data[i] for i in range(self.start, self.stop))

    def __eq__(self, other: StringView | str):
        if len(self) != len(other):
            return False
        for ch1, ch2 in zip(self, other):
            if ch1 != ch2:
                return False
        return True

    def __lt__(self, other: StringView | str):
        for ch1, ch2 in zip(self, other):
            if ch1 < ch2:
                return True
        if len(self) < len(other):
            return True
        return False


S = TypeVar('S', StringView, str)


def hamming_distance(kmer1: S, kmer2: S) -> int:
    mismatch = 0
    for ch1, ch2 in zip(kmer1, kmer2):
        if ch1 != ch2:
            mismatch += 1
    return mismatch


# MARKDOWN
def to_seeds(
        seq: S,
        mismatches: int
) -> list[S]:
    seed_cnt = mismatches + 1
    len_per_seed = ceil(len(seq) / seed_cnt)
    ret = []
    for i in range(0, len(seq), len_per_seed):
        ret.append(seq[i:i+len_per_seed])
    return ret


def seed_extension(
        test_sequence: S,
        found_seq_idx: int,
        found_seed_idx: int,
        seeds: list[S]
) -> tuple[int, int] | None:
    prefix_len = sum(len(seeds[i]) for i in range(0, found_seed_idx))
    start_idx = found_seq_idx - prefix_len
    if start_idx < 0:
        return None  # report out-of-bounds
    seq_idx = start_idx
    dist = 0
    for seed in seeds:
        block = test_sequence[seq_idx:seq_idx + len(seed)]
        if len(block) < len(seed):
            return None  # report out-of-bounds
        dist += hamming_distance(seed, block)
        seq_idx += len(seed)
    return start_idx, dist
# MARKDOWN
