# Exercise Break: Compute the Count arrays for BWT("abracadabra$").
#
# MY ANSWER
# ---------
import functools
from collections import Counter

from helpers.Utils import slide_window


def raw_cmp(a: str, b: str):
    for a_ch, b_ch in zip(a, b):
        if a_ch == '$' and b_ch == '$':
            continue
        if a_ch == '$':
            return -1
        if b_ch == '$':
            return 1
        if a_ch < b_ch:
            return -1
        if a_ch > b_ch:
            return 1
    if len(a) < len(b):
        return -1
    elif len(b) < len(a):
        return 1
    return 0


def bwt(text: str):
    matrix = [t for t, _ in slide_window(text, len(text), cyclic=True)]
    matrix.sort(key=functools.cmp_to_key(raw_cmp))
    return ''.join(row[-1] for row in matrix)


def count(idx: int, last_col: str):
    ret = Counter()
    for ch in last_col[:idx]:
        ret[ch] += 1
    return ret


# text = 'abracadabra$'
# matrix = bwt(text)
# last_col = ''.join(row[-1] for row in matrix)
last_col = 'smnpbnnaaaaa$a'
for i in range(len(last_col) + 1):
    print(f'{count(i, last_col)}')

