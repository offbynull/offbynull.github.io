# Exercise Break: Prove that SuffixTree(Text) has exactly |Text| leaves and at most |Text| other nodes.
#
# MY ANSWER
# ---------
# The first part "Prove that SuffixTree(Text) has exactly |Text| leaves":
# -----------------------------------------------------------------------
# It must have as many leaves as there are characters because that's how many unique suffixes there are in the string
# once you add in the special termination marker. The special termination marker makes it so that limbs aren't shared.
#
# The second part "and at most |Text| other nodes":
# -------------------------------------------------
# The definition of a tree is that internal nodes (not root or leaves, but the ones inbetween) can only ever fan out.
# Each internal node can only ever have a single input but has 1 or more outputs. So if the number of leaf nodes is
# |Text|, the number of internal nodes mus tbe <= |Text|
