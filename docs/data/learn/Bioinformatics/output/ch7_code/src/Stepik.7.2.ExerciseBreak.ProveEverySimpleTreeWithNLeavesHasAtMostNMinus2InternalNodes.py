# Exercise Break: Prove that every simple tree with n leaves has at most n - 2 internal nodes.

# FROM THE BOOK: we say that a path in a tree is __non-branching__ if every node other than the beginning and ending
# node of the path has degree equal to 2. A __non-branching__ path is __maximal__ if it is not a subpath of an even
# longer __non-branching__ path. If we substitute every __maximal non-branching__ path by a single edge whose length is
# equal to the length of the path, then the tree in figure on top becomes the tree in figure on the bottom. In general,
# after such a transformation, there are no nodes of degree 2; a tree satisfying this property is called a
# __simple tree__.

# ANSWER
# ------
#
# n=2, when n=2 you can have at most 2-2=0 internal nodes, this graph has 0 internal nodes, 0<=0 (TRUE)
# *---*
#
# n=3, when n=3 you can have at most 3-2=1 internal nodes, this graph has 1 internal node, 1<=1 (TRUE)
# *   *
#  \ /
#   *
#
# n=4, when n=4 you can have at most 4-2=2 internal nodes, this graph has 2 internal nodes, 2<=2 (TRUE)
# *   *
#  \ /
#   *
#   |
#   *
#  / \
# *   *
#
# n=4, when n=4 you can have at most 4-2=2 internal nodes, this graph has 1 internal node, 1<=2 (TRUE)
#    *
#    |
# *--*--*
#    |
#    *
#
#
# So what's the "proof" here? If it's a "simple tree" that means all the leaf nodes would be at a fork structures (as in
# n=3 diagram) and the internal nodes would either forks or straight lines (as shown for diagrams for n=4). For example,
# for n=5...
#    *
#    |
# *--*--*
#    |
#    *
#   / \
#  *   *
# when n=5 you can have at most 5-2=3 internal nodes, this graph has 2 internal nodes, 2<=3 (TRUE)
#
# Another example of n=5...
# *   *
#  \ /
#   *
#   |
#   *
#  / \
# *   *
#    / \
#   *   *
# when n=5 you can have at most 5-2=3 internal nodes, this graph has 3 internal nodes, 3<=3 (TRUE)
