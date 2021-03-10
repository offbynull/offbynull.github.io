# Exercise Break: How many permutations of length 10 have the property that no reversal applied to P decreases
# Breakpoints(P)?

# Breakpoint is defined as a adjacent pair in the permutation where the 2nd value is NOT 1 ahead of the first: (n, n+1)
# Do tests for smaller dimensions and try to pick out a pattern...
from itertools import permutations, product
from typing import List

from helpers.Utils import slide_window


def count_adj(p: List[int]) -> int:
    return sum(1 if x1 + 1 == x2 else 0 for (x1, x2), _ in slide_window(p, 2))


def count_bp(p: List[int]) -> int:
    return sum(0 if x1 + 1 == x2 else 1 for (x1, x2), _ in slide_window(p, 2))


def test(count: int):
    found = set()
    for n in permutations(range(0, count + 2)):  # instead of 1 to n, the chapter now says to make it 0 to n+1 where 0 and n+1 are implied AND fixed into place
        for signed_n in product(*([n[i], -n[i]] for i in range(len(n)))):
            if signed_n[0] != 0 or signed_n[-1] != count + 1:  # 0 and n+1 must be fixed into place at first and last idx respectively
                continue
            no_reversal_decremented_signed_n = True
            orig_bp = count_bp(list(signed_n))
            for i, j in product(range(1, len(signed_n) - 1), repeat=2):   # 0 and n+1 must be fixed into place at first and last idx respectively -- can't be reversed
                if i > j:
                    continue
                signed_n_with_reversal = list(signed_n)
                signed_n_with_reversal[i:j+1] = [-x for x in reversed(signed_n_with_reversal[i:j+1])]
                new_bp = count_bp(signed_n_with_reversal)
                if new_bp < orig_bp:
                    no_reversal_decremented_signed_n = False
                    break
            if no_reversal_decremented_signed_n:
                found.add(signed_n)
    # print(f'{len(found)} -- {found}')
    print(f'Ps where no reversal decrements breakpoints: {len(found)}')


test(1)  # Ps where no reversal decrements breakpoints: 1
test(2)  # Ps where no reversal decrements breakpoints: 2
test(3)  # Ps where no reversal decrements breakpoints: 6
test(4)  # Ps where no reversal decrements breakpoints: 24
test(5)  # Ps where no reversal decrements breakpoints: 120

# The pattern seems to be n!. So, for 10, the answer is 10! = 3628800

