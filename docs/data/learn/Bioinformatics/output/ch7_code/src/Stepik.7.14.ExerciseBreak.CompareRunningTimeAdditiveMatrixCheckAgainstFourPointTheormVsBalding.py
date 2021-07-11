# EXERCISE BREAK
#
# Exercise Break: Compare the running time of this proposed method (four point theorem) with that of a variant of
# AdditivePhylogeny deciding whether a given distance matrix is additive.

# ANSWER
# ------
# The four point model requires that you check every combo of 4 leaf nodes, right? It's 12 tests for each 4 tuple:
# P(4,2) = 12? So if you have n leaf nodes, that'd be O(n^4) quartets?
#
# The additive phylogeny model requires you to recursively bald a matrix, where at each recursive step you do an
# additive check that tests the last leaf node in the matrix against pairs in the matrix. At each recursive step you
# have to...
#
#   Calculate the limb length -- the algo the book gave had this at O(n^2), but the exercise break got it to O(n)
#   Bald the matrix -- O(n)
#   Find Additive Distance test -- O(n)
#
# That's 2*O(n) * O(n^2) at each recursive step, but simplify it to just O(n^2).
#
# It does the stuff above n-1 times (recurses), where at each step the n of the stuff in that recursive step drops by 1.
# Simplify that to O(n) * O(n^2). So that'd be O(n^3)?
#
# Not sure if this is entirely correct. I'm probably missing something here.
