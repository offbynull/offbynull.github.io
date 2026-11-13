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


def inverse_bwt(last_col: str):
    # index last_col
    c = Counter()
    last_col_indexed = []
    for ch in last_col:
        last_col_indexed.append((ch, c[ch]))
        c[ch] += 1
    # sort to get firsT_col
    first_col_indexed = sorted(last_col_indexed, key=functools.cmp_to_key(cmp))
    # match it up
    fc_idx = 0  # idx 0 must start with $ after getting sorted
    first_row = []
    first_row_remaining = len(last_col)
    while first_row_remaining > 0:
        next_ch = first_col_indexed[fc_idx]
        first_row.append(next_ch)
        fc_idx = last_col_indexed.index(next_ch)
        first_row_remaining -= 1
    orig_str = next(rotate_left(first_row))
    return ''.join(ch for ch, _ in orig_str)





with open('/home/user/Downloads/dataset_240382_11.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
text = data[0].strip()
result = inverse_bwt(text)
print(result)


