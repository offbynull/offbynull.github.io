# Exercise Break: Modify the coloring algorithm to find the longest shared substring of more than two strings.
#
# MY ANSWER
# --------
# I suspect you just need a different n different end markers (one for each string), and instead of using colors to
# determine the existence of nodes in a string, you can use a bitset (flip the bits on for the strings involved)
