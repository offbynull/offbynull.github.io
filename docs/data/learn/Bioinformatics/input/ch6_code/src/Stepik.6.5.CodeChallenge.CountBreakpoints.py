from typing import List

from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240320_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
signed_permutation = [int(i) for i in lines[0].split()]


def count_bp(p: List[int]) -> int:
    # instead of 1 to n, the chapter now says to make it 0 to n+1 where 0 and n+1 are implied AND fixed into place
    p = [0] + p + [len(p) + 1]
    return sum(0 if x1 + 1 == x2 else 1 for (x1, x2), _ in slide_window(p, 2))


print(f'{count_bp(signed_permutation)}')


# The section immediately after this question has a STOP and THINK question: We defined a breakpoint between an
# arbitrary permutation and the identity permutation. Generalize the notion of a breakpoint between two arbitrary
# permutations, and design a linear-time algorithm for computing this number.
#
#
#
# If you were to try to do this in using an algorithm that DOESN'T run in linear-time, the process would involve taking
# one of the permutations and finding+applying the necessary reversals until it ended up as the identity permutaiton. As
# you apply the reversals to the permutation, you apply the same reversal to the corresponding regions in the other
# permutation as well. For example, ...
#
#   -4 +3 -2 -1
#    |  |  |  |
#   +2 +1 +3 +4
#
# Reverse the entire thing to get ...
#
#   +1 +2 -3 +4
#    |  |  |  |
#   -4 -3 -1 -2
#
# Reverse -3 to get...
#
#   +1 +2 +3 +4
#    |  |  |  |
#   -4 -3 +1 -2
#
# The above has 2 breakpoints (not counting the implied 0 at the beginning and the implied n+1 at the end).
#
#
#
# To get the same result in linear time, I think what you have to do is pick one of the permutations and individually
# drag each element to the correct position for an identity permutation, reversing the element if necessary. As you
# apply these transformations to the first permutation, you mirror it on the second permutation. The same example above
# would be transformed as follows...
#
#   -4 +3 -2 -1
#    |  |  |  |
#   +2 +1 +3 +4
#
# Move -1 to the beginning and reverse it. When you reverse it, the other one reverses as well...
#
#   +1 -4 +3 -2
#    |  |  |  |
#   -4 +2 +1 +3
#
# Move -2 to the 2nd position and reverse it. When you reverse it, the other one reverses as well...
#
#   +1 +2 -4 +3
#    |  |  |  |
#   -4 -3 +2 +1
#
# Move +3 to the 3rd position...
#
#   +1 +2 +3 -4
#    |  |  |  |
#   -4 -3 +1 +2
#
# Reverse -4. When you reverse it, the other one reverses as well...
#
#   +1 +2 +3 +4
#    |  |  |  |
#   -4 -3 +1 -2
#
# The above has 2 breakpoints (not counting the implied 0 at the beginning and the implied n+1 at the end).
#
#
#
# Notice that the permutations end up exactly the same between the two algorithms. They have the same number of
# breakpoints. If you were to do the same thing again, but this time sort the bottom permutation to the the identity
# permutation, you'd get...
#
#   +3 -4 -2 -1
#    |  |  |  |
#   +1 +2 +3 +4
#
# The top permutation also ends up with 2 breakpoints (not counting the implied 0 at the beginning and the implied n+1
# at the end).
#
# Assuming my reasoning is correct, do we say that there are 2 breakpoints? If you think about the example as actually
# 3 permutations (top to identity to bottom), should the number actually be the breakpoint count  in top and bottom
# individually?
