# ￼Exercise Break: Show that the number of edges in the Viterbi graph of an HMM emitting a string of length n is
# |States|^2 * (n − 1) + 2 * |States|.


# MY ANSWER
# ---------
# 1. The number of edges for each state node to its child is |State| (one edge for each state transition)
# 2. The number of edges for each state "layer" to the next is |State| * |State| = |State|^2 (there are |State| nodes
#    in that layer, and each has |State| edges are discussed in 1).
# 3. Since n symbols being emitted, there are n-1 state transitions occurring / n-1 layers: |State|^2*(n-1)
# 4. There are |States| edges from going to SOURCE to first layer
# 4. There are |States| edges from going to SINK to last layer  (that's what I'm assuming is the case even though thats
#    not how my previous exercise problem was coded -- I had |State| edges from each node to the sink node, which would
#    be |State|^2 edges)
#
#        F---F---F---F--.
#       / \ / \ / \ / \ |
# SOURCE   X   X   X   SINK
#       \ / \ / \ / \ / |
#        B---B---B---B--'
#          H   H   T   T
#
# This is coming out at 18 edges where the algorithm is saying it expects 16 edges.
#
# I think there's a typo in the book. What it's actually expecting is |States|^2 * n + 2 * |States|
#
#        F---F---F---F---F
#       / \ / \ / \ / \ / \
# SOURCE   X   X   X   X   SINK
#       \ / \ / \ / \ / \ /
#        B---B---B---B---B
#          H   H   T   T
#
# |States|^2 * n is for the grid, 2 * |States| is from the edges from SOURCE and edges to SINK (which would both be set
# to not effect the final weight of a path).
