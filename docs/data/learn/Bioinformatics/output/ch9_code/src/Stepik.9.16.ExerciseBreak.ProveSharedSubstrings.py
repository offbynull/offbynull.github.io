# Exercise Break: Prove that a path ending in a purple node in the suffix tree of Text1 and Text2 spells out a substring
# shared by Text1 and Text2.
#
# Text1 = panama
# Text2 = bananas
#
# Trie for concatenated text: panama#bananas$  (each text gets a special end marker)
#
# Limbs starting within Text1 have their leaf node colored blue (denoted as B) and those starting within Text2 have
# their leaf node colored red (denoted as P). An internal node is colored blue if all of its children are blue, red if
# all of its children are red, or purple if it's a mix.
#
# .---+-------------+-------------+--ROOT--+---------+-------+----.
# |$  |#            |a           b|        |m        |n      |p   |s
# R   |b   .----+---P--+-----.   a|        |a        |a      |a   |$
#     |a   |#   |m     |n    |s  n|        |#     .--P---.   |n   R
#     |n   |b   |a     |a    |$  a|        |b    m|  |n  |a  |a
#     |a   |a   |#  .--P--.  R   n|        |a    a|  |a  |$  |m
#     |n   |n   |b  |m |n |s     a|        |n    #|  |s  R   |a
#     |a   |a   |a  |a |a |$     s|        |a    b|  |$      |#
#     |s   |n   |n  |# |s R      $|        |n    a|  R       |b
#     |$   |a   |a  |b |$         R        |a    n|          |a
#     B    |s   |n  |a R                   |s    a|          |n
#          |$   |a  |n                     |$    n|          |a
#          B    |s  |a                     B     a|          |n
#               |$  |n                           s|          |a
#               B   |a                           $|          |s
#                   |s                            B          |$
#                   |$                                       B
#                   B
#
# MY ANSWER
# --------
# I don't know how to prove this, but the answer seems obvious. If a set of limbs has the same parent, and those limbs
# start at different substrings (colored purple, marked as P), the chain of nodes from that parent up to the root will
# be a shared substring between those limbs (it's the starting redundant portion of the suffix).
