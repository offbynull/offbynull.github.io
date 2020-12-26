#      3     2     4     0
#   0---->3---->5---->9---->9
#  1|    0|    2|    4|    3|
#   v  3  v  2  v  4  v  2  v
#   1---->4---->?---->?---->?
#  4|    6|    5|    2|    1|
#   v  0  v  7  v  3  v  4  v
#   5---->10--->?---->?---->?
#  4|    4|    5|    2|    1|
#   v  3  v  3  v  0  v  2  v
#   9---->14--->?---->?---->?
#  5|    6|    8|    5|    3|
#   v  1  v  3  v  2  v  2  v
#   14--->20--->?---->?---->?
#
#
#               ^
#               |
#       This column is si,2
#
# Compute the values for the nodes in si,2. The value for each node should be computed by taking the incoming edge with
# the highest source node_weight+edge_weight.
#
# s0,2 = 5 (it's already filled in)
# s1,2 = 7 (5+2)
# s2,2 = 17 (10+7)
# s3,2 = 22 (17+5)
# s4,2 = 30 (22+8)
#
# There is no code for this. You just look at the DAG and do it by hand.
