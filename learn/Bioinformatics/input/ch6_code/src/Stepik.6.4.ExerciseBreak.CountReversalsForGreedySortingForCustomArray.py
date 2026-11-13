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
# How many reversals does GreedySorting need to sort the permutation (+100 +99 ... +2 +1)?

# For 3...
# +3 +2 +1 -> -1 -2 -3
# -1 -2 -3 -> +1 -2 -3
# +1 -2 -3 -> +1 +2 -3
# +1 +2 -3 -> +1 +2 +3

# For 3 it's 3 + 1. For 100 it's probably 100 + 1.
