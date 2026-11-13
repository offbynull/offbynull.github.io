# EXERCISE BREAK
#
# This discussion implies a recursive algorithm for the Distance-Based Phylogeny Problem:
#
#     find a pair of neighboring leaves i and j by selecting the minimum element Di,j in the distance matrix;
#     replace i and j with their parent, and recompute the distances from this parent to all other leaves as described above;
#     solve the Distance-Based Phylogeny problem for the smaller tree;
#     add the previously removed leaves i and j back to the tree.
#
# Apply this recursive approach to the additive distance matrix shown in the figure below. (Solve this exercise by hand.)

# DISTANCE MATRIX IS AS FOLLOWS:
#
#   |    | v1 | v2 | v3 | v4 |
#   |----|----|----|----|----|
#   | v1 | 0  | 13 | 21 | 22 |
#   | v2 | 13 | 0  | 12 | 13 |
#   | v3 | 21 | 12 | 0  | 13 |
#   | v4 | 22 | 13 | 13 | 0  |

# Iteration 1: smallest distance is between v2 and v3 ...
#
#   v2 *
#       \
#     r1 *---- ...
#       /
#   v3 *
#
#   dist(r1,v1) = (dist(v2,v1) + dist(v3,v1) - dist(v2,v3)) / 2 = (13 + 21 - 12) / 2 = 11
#   dist(r1,v4) = (dist(v2,v4) + dist(v3,v4) - dist(v2,v3)) / 2 = (13 + 13 - 12) / 2 = 7
#
# .. resulting in the reduced distance matrix...
#
#   |    | v1 | r1 | v4 |
#   |----|----|----|----|
#   | v1 | 0  | 11 | 22 |
#   | r1 | 11 | 0  | 7  |
#   | v4 | 22 | 7  | 0  |

# Iteration 2: smallest distance is between r1 and v4, but this is a 3 node tree, meaning that rather than continuing
#              the replacing operation we should just calculate the distance between all edges...
#
#             * v1
#            /
#   r1 *----* r2
#            \
#             * v4
#
#   dist(r2,v1) = (dist(v1,r1) + dist(v1,v4) - dist(r1,v4)) / 2 = (11 + 22 - 7) / 2 = 13
#   dist(r2,v4) = (dist(v1,r1) + dist(v1,v4) - dist(r1,v1)) / 2 = (11 + 22 - 11) / 2 = 11
#   dist(r2,r1) = (dist(v1,r1) + dist(r1,v4) - dist(v1,v4)) / 2 = (11 + 7 - 22) / 2 = -4   <-- THIS ISN'T POSSIBLE BECAUSE YOU CAN'T HAVE A NEGATIVE WEIGHT

# ??????????? Why is this not working, the book gives the following explanation: If you attempted the preceding
# exercise, then you were likely driven crazy. The reason why is that in the first step of our proposed algorithm, we
# assumed that a minimum element of an additive distance matrix corresponds to neighboring leaves. Yet as illustrated in
# figure below, this assumption is not necessarily true! Thus, we need a new approach to the Distance-Based Phylogeny
# Problem, as finding the animal coronavirus that is the smallest distance from SARS-CoV may not be the best way to
# identify the animal reservoir of SARS.
#
# THE MEANING OF THE ABOVE IS THAT THIS RECURSIVE ALGORITHM WON'T WORK IN EVERY CASE
