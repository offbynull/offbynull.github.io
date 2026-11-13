# Exercise Break: Prove that if Di,j is equal to the number of differing symbols between rows i and j in a multiple alignment, then D is symmetric, non-negative, and satisfies the triangle inequality.

# ANSWER
#
# In this case, "differing symbols between rows i and j" just means hamming distance between sequences, so if you have
# 4 sequences...
#
#   1: ACTGTTGT
#   2: CCTGATGT
#   3: ACCCTTCT
#   4: GCTGTTCT
#
# Di,j of i=1 and j=4 would be 2...
#
#   1: ACTGTTGT
#   4: GCTGTTCT
#      X     X
#
# CRITERIA 1: D is symmetric (Di,j == Dj,i)
# -----------------------------------------
# The hamming distance will always be the same regardless of the order. In the example above, D1,4 == D4,1
#
# CRITERIA 2: D is non-negative (Di,j >= 0)
# -----------------------------------------
# The hamming distance will always be non-negative. That's because you can never have a negative number of differences.
# At a minimum, there are 0 differences between two sequences (they're the same sequence).
#
# CRITERIA 3: D satisfies the triangle inequality (Di,j + Dj,k ≥ Di,k)
# --------------------------------------------------------------------
# This one makes no sense. If you take the matrix from the page prior...
#
#           Chimp  Human  Seal  Whale
#    Chimp    0      3     6      4
#    Human    3      0     7      5
#    Seal     6      7     0      2
#    Whale    4      5     2      0
#
# And apply i=0,j=1,k=2...
#
#    Di,j = D0,1 = 3
#    Dj,k = D1,2 = 7
#    Di,k = D0,2 = 6
#
# 3 + 7 >= 6      THIS IS FALSE. The author probably explained this one wrong.
