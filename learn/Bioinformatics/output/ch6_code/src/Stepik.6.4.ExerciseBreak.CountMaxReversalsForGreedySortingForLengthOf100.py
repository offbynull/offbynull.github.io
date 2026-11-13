#     GreedySorting(P)
#         approxReversalDistance ← 0
#         for k = 1 to |P|
#             if element k is not sorted
#                 apply the k-sorting reversal to P
#                 approxReversalDistance ← approxReversalDistance + 1
#             if k-th element of P is −k
#                 apply the k-sorting reversal to P
#                 approxReversalDistance ← approxReversalDistance + 1
#         return approxReversalDistance
#
# What is the largest number of reversals that GreedySorting could ever require to sort a permutation of length 100?

# For 3...
# -3 +1 +2 -> -1 +3 +2
# -1 +3 +2 -> +1 +3 +2
# +1 +3 +2 -> +1 -2 -3
# +1 -2 -3 -> +1 +2 -3
# +1 +2 -3 -> +1 +2 +3

# For 3 it's 5. The pattern to creating max reversal count seems to be splitting a sorted P into 2, reversing the second
# half, then interleaving it? Do some further experiments to verify...
from itertools import product, permutations
from typing import List


def greedy_sorting(p: List[int]):
    p = p[:]
    for start in range(0, len(p)):
        k = start + 1
        # is the correct value in the correct slot already? skip
        if p[start] == k:
            continue
        # find where the correct value is
        end = -1
        for i, v in enumerate(p[start:]):
            if v == k or v == -k:
                end = start + i
                break
        # reverse the elements between start and end + negate each one, putting the correct value at start (although it might be negative) -- +1 STEPS
        p[start:end+1] = [-x for x in reversed(p[start:end+1])]
        yield p
        # if the newly placed correct value is negative, make it positive -- +1 STEPS
        if p[start] < 0:
            p[start] = -p[start]
            yield p


def test(count: int):
    max_steps = -1
    found = []
    for n in permutations(range(1, count + 1)):
        for signed_n in product(*([n[i], -n[i]] for i in range(len(n)))):
            steps = [s[:] for s in greedy_sorting(list(signed_n))]
            if len(steps) > max_steps:
                found = []
                max_steps = len(steps)
            if len(steps) == max_steps:
                found.append(signed_n)
    print(f'Max of {max_steps} reversals that came from {found}')


test(2)  # Max of 3 reversals that came from [(2, 1)]
test(3)  # Max of 5 reversals that came from [(-2, -3, 1), (-3, 1, 2)]
test(4)  # Max of 7 reversals that came from [(-2, 4, 1, 3), (-2, 4, 3, 1), (3, 1, -4, 2), (-3, -2, 4, 1), (4, 1, 2, 3), (4, 3, 1, 2)]
test(5)  # Max of 9 reversals that came from [(-2, -4, 1, -5, 3), (-2, -4, -5, 1, 3), (-2, -4, -5, 3, 1), (-2, -5, 1, 3, 4), (-2, -5, 3, 1, 4), (-2, -5, 3, 4, 1), (3, 1, 5, 2, 4), (3, 1, 5, 4, 2), (-3, -2, -4, -5, 1), (-3, -2, -5, 1, 4), (3, 4, 1, 5, 2), (-3, 5, -2, -4, 1), (-4, 1, 2, -5, 3), (4, 1, -3, 5, 2), (-4, -2, -5, 3, 1), (-4, -3, -2, -5, 1), (-4, -5, 1, 2, 3), (-4, -5, 3, 1, 2), (-5, 1, 2, 3, 4), (-5, 1, 4, 2, 3), (5, -2, -4, 1, 3), (-5, 3, 1, 2, 4), (-5, 3, 1, 4, 2), (-5, 3, 4, 1, 2)]

# I was wrong. The pattern seems to be that for a P of length n, the maximum number of reversals is P + P-1. So for 100,
# the answer is 100 + 99 = 199.
#
# Here's what I noticed from the outputs...
#   For odd lengths, the input P used to generate the maximum number of steps is [-n, 1, 2, 3, ...]
#   For even lengths, the input P used to generate the maximum number of steps is [n, 1, 2, 3, ...]
# No proof for either, just what I'm guessing from looking at the outputs for test(2) through to test(7)







# FROM THE NEXT SECTION...
#
# STOP and Think: Can you find a lower bound on drev(P)? For example, can you show that the mouse permutation
# (+1 −7 +6 −10 +9 −8 +2 −11 −3 +5 +4) cannot be sorted with fewer than seven reversals?

# drev(P) is the number of reversals required to get P into [1, 2, 3, 4, ..., n].
# I think the answer has to do with the number of contiguous incrementing / decrementing segments? For example, the
# lower bounds for (−6 +1 +2 +3 +4 +5) would be 2, because it has 2 contiguous incrementing / decrementing segments...
#   (−6) (+1 +2 +3 +4 +5)
# The real minimum reversals for (−6 +1 +2 +3 +4 +5) is 3, which is okay because its above our lowerbound...
#   (−6 +1 +2 +3 +4 +5)
#   (−5 −4 −3 −2 −1 +6)
#   (+1 +2 +3 +4 +5 +6)
#
# My answer is probably wrong. You can try doing tests similar to the one above to try and derive some pattern.
