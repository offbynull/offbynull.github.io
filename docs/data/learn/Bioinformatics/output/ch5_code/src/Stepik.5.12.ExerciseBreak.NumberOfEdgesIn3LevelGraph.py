# Exercise Break: Prove that the number of edges in the three-level graph described in the figure below is at most
# 7 · n · m for sequences of length n and m.
#
#
#
# Given a 6x6 graph (n=6, m=6)...
#
# lower layer has 6*5 edges
# middle layer has 5*5 edges
# upper layer has 5*6 edges
# middle layer to lower layer edges has 5*5
# lower layer to middle layer edges has 5*5
# middle layer to upper layer edges has 5*5
# upper layer to middle layer edges has 5*5
#
# So abstract it out: Given an nxm graph...
#
# lower layer has n*m-1 edges
# middle layer has n-1*m-1 edges
# upper layer has n-1*m edges
# middle layer to lower layer edges has n-1*m-1
# lower layer to middle layer edges has n-1*m-1
# middle layer to upper layer edges has n-1*m-1
# upper layer to middle layer edges has n-1*m-1
#
# n*m-1 + n-1*m-1 + n-1*m + n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 <= 7*n*m
# n*m-1 - n + n-1*m-1 + n-1*m + n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 <= 7*n*m - n
# n-1*m-1 + n-1*m-1 + n-1*m + n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 <= 7*n*m - n
# n-1*m-1 + n-1*m-1 + n-1*m - n-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 <= 7*n*m - n - n - 1
# n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 + n-1*m-1 <= 7*n*m - n - n - 1
# 7*n-1*m-1 <= 7*n*m - n - n - 1
# 7*n-1*m-1 <= 7*n*m - 2n - 1
# 7*n-1*m-1 + 2n + 1 <= 7*n*m

# I hope I didn't screw up the reasoning somewhere, but I think this is correct. For n and m of ...
# 0, it'll be 0 <= 0
# 1, it'll be 3 <= 7
# 2, it'll be 12 <= 28
# 3, ...
#
# As both sides grow from 0 onward, the rhs's growth is faster than the lhs's growth (steeper slope).

