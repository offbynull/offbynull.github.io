# Exercise Break: Construct the suffix trie for "papa" without first appending the dollar-sign to mark the end of the
# text. Where are the paths corresponding to each suffix of "papa"? Do you now see why we first append "$" to the end of
# the text? (Hint: try to locate the suffix "pa" in your trie).
#
# MY ANSWER
# ---------
#     p   a
#   *---*---*
# a/
# *
# p\
#   *
#   a\  p   a
#     *---*---*
#
#
# The end marker is ment for disambiguation. I did something similar by marking nodes with a terminator flag. Using
# this dollar sign marker...
#
#      *
#    $/ p   a   $
#    *---*---*---*
#   /
# a/ p  a   $
# *---*---*---*
# $\       \
#   *      p\  q    $
#            *---*---*
