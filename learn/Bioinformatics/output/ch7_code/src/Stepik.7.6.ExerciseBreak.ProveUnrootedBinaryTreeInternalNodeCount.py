# EXERCISE BREAK
# --------------
# Exercise Break: Prove that every unrooted binary tree with n leaves has n - 2 internal nodes (and thus 2n - 3 edges).
#
#                   *
#                  /
#    *    *       *--*
#     \   |      /
#      *--*--*--*
#     /      |   \
#    *       *    *


# MY ATTEMPT AT ANSWERING
# -----------------------
# Every leaf's limb connects it to an internal node, so len(internal_nodes) >= len(leaf_nodes)
# Every internal node is connected to 3 other nodes.
#
# If an internal node is connected to 2 leaf nodes, it must have 1 connection to another internal node
# If an internal node is connected to 1 leaf nodes, it must have 2 connection to another internal node
# If an internal node is connected to 0 leaf nodes, it must have 3 connection to another internal node
#
# For 3 leaf nodes, it must be 1 internal node...
#
#       *
#      /
# *---*
#      \
#       *
#
# For 4 leaf nodes, it must be 2 internal nodes...
#
# *       *
#  \     /
#   *---*
#  /     \
# *       *
#
# For 5 leaf nodes, it'd be the same as 4 leaf nodes but 1 new internal node would have to get injected between the
# edge connecting the existing internal nodes, then the 5th leaf node would branch out from that edge...
#
# *           *
#  \         /
#   *---*---*
#  /    |    \
# *     *     *
#
# And that's the crux of it. After 4 nodes, each new leaf is added by injecting a new internal node between an edge
# connecting existing internal nodes. Meaning...
#
#   1. at 4 leaf nodes, the number of internal nodes MUST be 2  (2 less than the number of leaf nodes: 4-2=2)
#   2. for each leaf node added (past 4), the number of internal nodes MUST increase by exactly 1 (e.g. if 4 leaf nodes
#   had 2 internal nodes, 5 leaf nodes will have 3, 6 leaf nodes will have 4, etc..)
#
# As such, the number of internal nodes is guaranteed to be len(leaf_nodes) - 2

# This isn't really a proof but some basic reasoning
