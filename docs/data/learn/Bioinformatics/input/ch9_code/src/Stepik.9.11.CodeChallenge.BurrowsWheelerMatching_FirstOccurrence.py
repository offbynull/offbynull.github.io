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


def has_char_instance(ch: str, top_c: Counter[str], bottom_c: Counter[str]):
    max = bottom_c[ch]
    min = top_c[ch]
    return max - min > 0


def bw_matching(last_col: str, pattern: str, first_occurrence: dict[str, int], counts: list[Counter[str]]):
    top = 0
    bottom = len(last_col) - 1
    while top <= bottom:
        if pattern != '':
            ch = pattern[-1]
            pattern = pattern[:-1]
            if has_char_instance(ch, counts[top], counts[bottom+1]):
                top = first_occurrence[ch] + counts[top][ch]
                bottom = first_occurrence[ch] + counts[bottom + 1][ch] - 1
            else:
                return 0
        else:
            return bottom - top + 1
    raise ValueError('???')


def create_counts(last_col: str):
    ret = []
    for i in range(len(last_col) + 1):
        counts = Counter()
        for ch in last_col[:i]:
            counts[ch] += 1
        ret.append(counts)
    return ret


def create_first_occurrence(last_col: str):
    c = Counter()
    last_col_indexed = []
    for ch in last_col:
        last_col_indexed.append((ch, c[ch]))
        c[ch] += 1
    first_col_indexed = sorted(last_col_indexed, key=functools.cmp_to_key(cmp))
    first_occurrence = {}
    for i, (ch, cnt) in enumerate(first_col_indexed):
        if cnt == 0:
            first_occurrence[ch] = i
    return first_occurrence





with open('/home/user/Downloads/dataset_240384_7.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
last_col = data[0].strip()
patterns = data[1].strip().split()

first_occurrence = create_first_occurrence(last_col)
counts = create_counts(last_col)
result = [bw_matching(last_col, p, first_occurrence, counts) for p in patterns]
print(' '.join(str(c) for c in result))


