# Synteny blocks have direction. Because they have direction, when they're indexed a sign is added to represent that
# direction. For example, the block at index 1 can either be +1 or -1 depending on if its forward or revere
# (respective).
#
# Count the permutations for a set of 7 synteny blocks. For example, the 3 synteny blocks...
#   +A +B +C
# may end up as...
#   -B +A -C
#
# This is basically permutations without repetition. For example, if you wanted to count the number of permutations for
# the set {A, B, C}, it'd be 3!: The number of options at ...
#   * index 0 is 3 (either A, B or C)
#   * index 1 is 2 (the item selected in the last step isn't available for this step)
#   * index 2 is 1 (the items selected in the last 2 steps isn't available for this step)
# 3! = 3*2*1 = 6.
#
# Since synteny blocks have a direction/sign, that needs to be accounted for in the calculation. In the example above,
# a set of 3 synteny blocks would be represented as the set {+A, -A, +B, -B, +C, -C}. Once a specific block is selected,
# both its directions are removed before moving on to the next step (e.g. if -A was selected at for index 0, both +A and
# -A are removed for the next step).  The number of options at ...
#   * index 0 is 6 (either +A, +B, +C, -A, -B, or -C)
#   * index 1 is 4 (both the + and - version of item selected in the last step isn't available for this step)
#   * index 2 is 2 (both the + and - version of the items selected in the last 2 steps isn't available for this step)
# 6*4*2 = 6.
#
# For 7 synteny blocks...
from math import factorial

print(f'{14*12*10*8*6*4*2}')
print(f'{2**7 * factorial(7)}')
