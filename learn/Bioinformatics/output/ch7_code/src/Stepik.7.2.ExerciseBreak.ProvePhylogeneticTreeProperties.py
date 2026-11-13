# EXERCISE BREAK
#
# Prove the following statements:
#
#     1. Every tree with at least two nodes has at least two leaves.
#     2. Every tree with n nodes has n - 1 edges;
#     3. there exists exactly one path connecting every pair of nodes in a tree. Hint: what would happen if there were two different paths connecting a pair of nodes? What would happen if there were no paths connecting a pair of nodes?


# ANSWER
#
# Recall that a phylogenetic tree CANNOT be cyclic (it's a tree) and is a connected graph (a path exists between every
# node and every other node). It is not a directed graph, therefore it doesn't qualify as being a DAG.
#
# CRITERIA 1: Every tree with at least two nodes has at least two leaves.
# -----------------------------------------------------------------------
# A leaf is a node with a degree of 1 (exactly 1 edge)
#
# 1 node tree:
#    *
#
# 2 node tree:
#    *-----*
#    both nodes have a degree of 1, as such they're both leaf nodes
#
# 3 node tree:
#   *------*
#    \
#     \
#      *
#   2 nodes have a degree of 1, as such 2 nodes are leaf nodes
#
# 4 node trees:
#   *------*-----*     *-------*------*      *-----*-----*-----*
#    \                          \
#     \                          \
#      *                          *
#   first one has 2 leaves, second one has 3 leaves, 3rd one has 2 leaves
#
# For an n node graph, the worst case is a linear chain -- both end of the chain will hae a degree of 1, meaning they're
# both leaves.
#
#
# CRITERIA 2: Every tree with n nodes has n - 1 edges
# ---------------------------------------------------
# Starting from the a root node, it fans out to 1 level to child nodes, then each child at level 1 fans out to child
# nodes at level 2, etc.. At each node, fan out to m other child nodes requires m edges. So, for example, ...
#
#   Root fans out to 5 nodes
#     Child 1 fans out to 3 leaf nodes
#     Child 2 fans out to 2 leaf nodes
#     Child 3 fans out to 4 leaf nodes
#     Child 4 fans out to 2 nodes
#       Child 4.1 fans out to 3 leaf nodes
#       Child 4.2 fans out to 2 leaf nodes
#
# At each leave, each child node being fanned out to by a parent node requires 1 edge, so that means each child gets
# assigned an edge. Except for the initial root node that first fans out -- that's nobody's child.
#
# If each child node gets an edge except for the root, that means that there are n-1 edges in a graph that has n nodes.
#
#
# CRITERIA 3: there exists exactly one path connecting every pair of nodes in a tree
# ----------------------------------------------------------------------------------
# Recall that this is not a direct graph, so if you have more than 1 path to a node, you'll get a cycle. For example,
# take the following graph...
#
#      A-------B-------C-------D
#               \
#                \
#                 E
#
# ... and add a second path from B to D...
#
#                -------------
#               /             \
#      A-------B-------C-------D
#               \
#                \
#                 E
#
# There's now a cycle: B-C-D-B

