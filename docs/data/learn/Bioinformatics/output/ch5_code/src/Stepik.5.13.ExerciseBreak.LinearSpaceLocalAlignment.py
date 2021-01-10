# Recall the concept of free-ride edges - each node in a local alignment graph has an edge coming from the top-left node
# (with score 0) and an edge going to the bottom right node (with score FINAL WEIGHT).
#
# This implementation is the same as the linear space global alignment implementation (code challenge 5.13), but it
# needs extra logic to simulate...
#   * edges coming from (0,0), the weight at each node must be at least 0: weight = max(0,weight)
#   * edges going to (LAST, LAST), the weight must be the max weight of all other nodes: weight = max(all_node_weights)
#
# The algorithm needs to account for node jumps. If it detects that the node was jumped to from (0,0), it should
# subdivide starting from that node all the way to the bottom. As it subdivides, it should keep track of node weights it
# finds via find_middle_edge. The node with the maximum weight is the termination point -- it jumps all the way to the
# bottom
#
# I'm not sure if anything else needs to be updated?
#
# There is no code for this -- it asked for a design, not an implementation.
