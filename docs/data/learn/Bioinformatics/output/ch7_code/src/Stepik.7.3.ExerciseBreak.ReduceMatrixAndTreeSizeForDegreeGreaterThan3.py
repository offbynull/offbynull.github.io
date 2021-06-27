# EXERCISE BREAK
#
# Exercise Break: We have just described how to reduce the size of the tree as well as the dimension of the distance
# matrix D if the parent node (m) has degree 3. Design a similar approach in the case that the degree of m is larger
# than 3.


# Recall that for m having a degree of 3...
#
#    i *           * k
#       \         /
#      m *-------*
#       /         \
#    j *           * l
#
#   |   | i | j | k | l |
#   |---|---|---|---|---|
#   | i | ? | ? | ? | ? |
#   | j | ? | ? | ? | ? |
#   | k | ? | ? | ? | ? |
#   | l | ? | ? | ? | ? |
#
# ... you can remove the leaf nodes i and j, leaving you with a new leaf node of just m. This is possible because the
# distance between m and other leaf nodes may be derived just from the weights in the original matrix...
#
#   dist(m,k) = (dist(i,k) + dist(j,k) - dist(i,j)) / 2
#   dist(m,l) = (dist(i,l) + dist(j,l) - dist(i,j)) / 2
#
# Once these distances have been calculated, you can remove i and j from the tree and replace them in the distance
# matrix with just m...
#
#                  * k
#                 /
#      m *-------*
#                 \
#                 * l
#
#   |   | m | k | l |
#   |---|---|---|---|
#   | m | ? | ? | ? |
#   | k | ? | ? | ? |
#   | l | ? | ? | ? |

#
# ANSWER
#
# How would this work if m had a degree of 4?
#
#             * a
#            /
#           *
#    i *   / \
#       \ /   * b
#      m *
#       / \   * c
#    j *   \ /
#           *
#            \
#             * d
#
#   |   | i | j | a | b | c | d |
#   |---|---|---|---|---|---|---|
#   | i | ? | ? | ? | ? | ? | ? |
#   | j | ? | ? | ? | ? | ? | ? |
#   | a | ? | ? | ? | ? | ? | ? |
#   | b | ? | ? | ? | ? | ? | ? |
#   | c | ? | ? | ? | ? | ? | ? |
#   | d | ? | ? | ? | ? | ? | ? |
#
# Do the same thing as before: Calculate the distance from m to every other leaf node just as you did for degree = 3...
#
#   dist(m,a) = (dist(i,a) + dist(j,a) - dist(i,j)) / 2
#   dist(m,b) = (dist(i,b) + dist(j,b) - dist(i,j)) / 2
#   dist(m,c) = (dist(i,c) + dist(j,c) - dist(i,j)) / 2
#   dist(m,d) = (dist(i,d) + dist(j,d) - dist(i,j)) / 2
#
# ... which ends up resulting in...
#
#             * a
#            /
#           *
#          / \
#         /   * b
#      m *
#         \   * c
#          \ /
#           *
#            \
#             * d
#
#   |   | m | a | b | c | d |
#   |---|---|---|---|---|---|
#   | m | ? | ? | ? | ? | ? |
#   | a | ? | ? | ? | ? | ? |
#   | b | ? | ? | ? | ? | ? |
#   | c | ? | ? | ? | ? | ? |
#   | d | ? | ? | ? | ? | ? |
#
# I'm fairly certain this is right, but I haven't tested it out.
