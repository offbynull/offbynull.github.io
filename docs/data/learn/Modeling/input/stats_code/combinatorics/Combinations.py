from collections import Counter
from itertools import product
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


# MARKDOWN_BINOMIAL_COEFFICIENTS
def binomial_coefficients(exp: int) -> list[int]:
    ret = []
    for r in range(exp + 1):
        c = count_combinations(exp, r)
        ret.append(c)
    return ret
# MARKDOWN_BINOMIAL_COEFFICIENTS


# MARKDOWN_MULTINOMIAL_COEFFICIENTS
def multinomial_coefficient(exp: int, group_counts: list[int]) -> int:
    assert sum(group_counts) == exp
    num = factorial(exp)
    denom = 1
    for g in group_counts:
        denom *= factorial(g)
    return num // denom


def multinomial_coefficients(exp: int, nomial_count: int) -> list[int]:
    ret = []
    for term_exponents in product(range(exp+1), repeat=nomial_count):
        term_exponents = list(term_exponents)
        if sum(term_exponents) != exp:
            continue
        c = multinomial_coefficient(exp, term_exponents)
        ret.append(c)
    return ret
# MARKDOWN_MULTINOMIAL_COEFFICIENTS


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
