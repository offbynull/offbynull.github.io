# Exercise Break: Compute the number of partitions of n points into two non-empty clusters.
#
#
#
# MY ANSWER
# ----------
#
# I think this is asking for is the different number of ways n points can be partitioned into 2 (where each partition is
# non-empty). In other words, a set of n points to 2 distinct non-empty sets that have no overlapping elements.
#
# ABC
#    A | BC
#    AB | C
#    B | AC
#
# ABCD
#    A | BCD
#    B | ACD
#    C | ABD
#    D | ABC
#    AB | CD
#    AC | BD
#    AD | BC
#
#
# CODE IT OUT INSTEAD...

from itertools import permutations

test_str = 'ABCDEFGHIJ'
final = set()
for i in range(len(test_str)):
    for x in permutations(set(test_str), r=len(test_str)):
        s1 = frozenset(x[:i])
        s2 = frozenset(x[i:])
        if not s1 or not s2:
            continue
        final.add(frozenset({s1, s2}))
for s1, s2 in final:
    print(f'{s1} {s2}')
print(f'{len(final)}')

# The answers from running the code above with different length inputs...
#
# len(2) == 1 different ways to partition
# len(3) == 3 different ways to partition
# len(4) == 7 different ways to partition
# len(5) == 15 different ways to partition
# len(6) == 31 different ways to partition
# len(7) == 63 different ways to partition
# len(8) == 127 different ways to partition
# len(9) == 255 different ways to partition
# len(10) = 511 different ways to partition
#
# What I think is happening:
#  The number of different ways to partition is 2^(len - 1) - 1
