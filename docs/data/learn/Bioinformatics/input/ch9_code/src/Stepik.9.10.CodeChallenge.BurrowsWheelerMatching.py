import functools
from collections import Counter

from helpers.Utils import slide_window, rotate_left


def cmp(a: tuple[str, int], b: tuple[str, int]):
    assert len(a[0]) == 1
    assert len(b[0]) == 1
    (a_ch, a_idx), (b_ch, b_idx) = a, b
    # compare against term symbol
    if a_ch == '$' and b_ch == '$':
        return 0
    if a_ch == '$':
        return -1
    if b_ch == '$':
        return 1
    # compare against each other
    if a_ch < b_ch:
        return -1
    if a_ch > b_ch:
        return 1
    # at this point, chars are equal, check idxes
    if a_idx < b_idx:
        return -1
    if a_idx > b_idx:
        return 1
    # at this point, chars and idxes are equal
    return 0


def bw_matching(last_col: str, pattern: str, last_to_first: list[int]):
    top = 0
    bottom = len(last_col) - 1
    while top <= bottom:
        if pattern != '':
            ch = pattern[-1]
            pattern = pattern[:-1]
            if last_col.find(ch, top, bottom + 1) != -1:
                top_idx = last_col.find(ch, top, bottom + 1)
                bottom_idx = last_col.rfind(ch, top, bottom + 1)
                top = last_to_first[top_idx]
                bottom = last_to_first[bottom_idx]
            else:
                return 0
        else:
            return bottom - top + 1
    raise ValueError('???')


def create_last_to_first(last_col: str):
    c = Counter()
    last_col_indexed = []
    for ch in last_col:
        last_col_indexed.append((ch, c[ch]))
        c[ch] += 1
    first_col_indexed = sorted(last_col_indexed, key=functools.cmp_to_key(cmp))
    last_to_first = [first_col_indexed.index(e) for e in last_col_indexed]
    return last_to_first





with open('/home/user/Downloads/dataset_240383_8.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
last_col = data[0].strip()
patterns = data[1].strip().split()

last_to_first_idx = create_last_to_first(last_col)
result = [bw_matching(last_col, p, last_to_first_idx) for p in patterns]
print(' '.join(str(c) for c in result))


