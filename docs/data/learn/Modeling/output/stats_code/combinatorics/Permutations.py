from collections import Counter
from math import factorial
from sys import stdin
from typing import Any


# MARKDOWN_NORMAL
def count_permutations(n: int) -> int:
    return factorial(n)
# MARKDOWN_NORMAL

# MARKDOWN_GROUPED
def count_grouped_permutations(n_list: list[int]) -> int:
    k = len(n_list)
    product = 1
    for n in n_list:
        product *= count_permutations(n)
    product *= k
    return product
# MARKDOWN_GROUPED

# MARKDOWN_REPETITIONS
# Each index in object_repetitions represents a unique object, where the value at that index is the number of times that
# object repeats. For example, PEPPER may be represented as [1,3,1], where index ...
#  * 1 is the repetition count for E (2 time)
#  * 2 is the repetition count for P (3 times)
#  * 3 is the repetition count for R (1 time)
def count_permutations_with_repetitions(object_repetitions: list[int]) -> int:
    numerator = count_permutations(sum(object_repetitions))
    denominator = 1
    for repetitions in object_repetitions:
        denominator *= count_permutations(repetitions)
    return numerator // denominator
# MARKDOWN_REPETITIONS


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
