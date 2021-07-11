# EXERCISE BREAK
#
# Exercise Break: Prove the Four Point Theorem.

# Definitions
# -----------
# Four Point Condition: Given leaf nodes (i, j, k, l) in an additive distance matrix, one pair of distances must be less
# than or equal to the remaining two pairs of distances. Those remaining two pairs must be equal. So for example, it may
# be that...
#   * dist(i,j) * dist(k,l) <= dist(i,k) + dist(j,l) == dist(i,l) + dist(j,k)
#   * or, dist(i,k) + dist(j,l) <= dist(i,j) * dist(k,l) == dist(i,l) + dist(j,k)
#   * or, dist(i,l) + dist(j,k) <= dist(i,j) * dist(k,l) == dist(i,k) + dist(j,l)
#   * or, ...
#
# Four Point Theorem: A distance matrix is additive if and only if the four point condition holds for every quartet
# (i, j, k, l) of indices of this matrix.

# Read the notes for a more elaborate discussion. The proof below makes sense if you see the diagram in the book.

# THIS MY ATTEMPT AT A PROOF (not really a proof)
# --------------------------
# In the simplest case, there would be no internal edges between the leaf quartet...
#    i *   * k
#       \ /
#      m *
#       / \
#    j *   * l
# No matter what the edge weights are here, the 4 points condition would be true. Either all sum would be = or one of
# the sums would be <= than the other two sums (which would be =).
#
# What about when there's 1 internal edge?...
#    i *           * k
#       \         /
#      m *-------*
#       /         \
#    j *           * l
# Assuming an edges can't have a 0 weight (why would they? a zero weight would be the species on both ends are equal),
# one sum will always be < the other two sums (which would be =). Adding more non-zero internal edges doesn't change
# that.
#
# If the edge can have 0 weight, then it's possible for one sum to be <= the other two sums, just like where the
# simplest case example above where no internal edges exist.
