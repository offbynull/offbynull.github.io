from collections import Counter
from math import factorial
from sys import stdin
from typing import Any


# MARKDOWN_NORMAL
def count_combinations(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    elif r == n or r == 0:
        return 1
    return factorial(n) // (factorial(n-r) * factorial(r))
# MARKDOWN_NORMAL


# MARKDOWN_INCLUDE
def count_combinations_with_include_restrictions(n: int, r: int, include_object_count: int) -> int:
    return count_combinations(n - include_object_count, r - include_object_count)
# MARKDOWN_INCLUDE


# MARKDOWN_EXCLUDE
def count_combinations_with_exclude_restrictions(n: int, r: int, exclude_object_count: int) -> int:
    return count_combinations(n, r) - count_combinations_with_include_restrictions(n, r, exclude_object_count)
# MARKDOWN_EXCLUDE


# MARKDOWN_PASCAL
def count_combinations_via_pascal_recurrence(n: int, r: int) -> int:
    if n == 0:
        return 1
    if r == 0 or r == n:
        return 1
    return count_combinations_via_pascal_recurrence(n - 1, r - 1)\
        + count_combinations_via_pascal_recurrence(n - 1, r)
# MARKDOWN_PASCAL


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        print('```')
        exec(data_raw)
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")
