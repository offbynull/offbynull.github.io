# Exercise Break: Reconstruct the string whose Burrows-Wheeler transform is "enwvpeoseu$llt". (Don't forget the $ at the
# end!)
#
# MY ANSWER
# ---------
# STEP1: "" is the LAST column of the matrix.
#
#   [ , , , , , , , , , , , , ,e]
#   [ , , , , , , , , , , , , ,n]
#   [ , , , , , , , , , , , , ,w]
#   [ , , , , , , , , , , , , ,v]
#   [ , , , , , , , , , , , , ,p]
#   [ , , , , , , , , , , , , ,e]
#   [ , , , , , , , , , , , , ,o]
#   [ , , , , , , , , , , , , ,s]
#   [ , , , , , , , , , , , , ,e]
#   [ , , , , , , , , , , , , ,u]
#   [ , , , , , , , , , , , , ,$]
#   [ , , , , , , , , , , , , ,l]
#   [ , , , , , , , , , , , , ,l]
#   [ , , , , , , , , , , , , ,t]
from helpers.Utils import rotate_left, rotate_right

last_col_str = "enwvpeoseu$llt"


# STEP2: SORT the last column to get the first column: "$eeellnopstuvw"
#
#   [$, , , , , , , , , , , , ,e]
#   [e, , , , , , , , , , , , ,n]
#   [e, , , , , , , , , , , , ,w]
#   [e, , , , , , , , , , , , ,v]
#   [l, , , , , , , , , , , , ,p]
#   [l, , , , , , , , , , , , ,e]
#   [n, , , , , , , , , , , , ,o]
#   [o, , , , , , , , , , , , ,s]
#   [p, , , , , , , , , , , , ,e]
#   [s, , , , , , , , , , , , ,u]
#   [t, , , , , , , , , , , , ,$]
#   [u, , , , , , , , , , , , ,l]
#   [v, , , , , , , , , , , , ,l]
#   [w, , , , , , , , , , , , ,t]

import functools


def cmp(a: str, b: str):
    for a_ch, b_ch in zip(a, b):
        if a_ch == '$' and b_ch == '$':
            continue
        if a_ch == '$':
            return -1
        if b_ch == '$':
            return 1
        if a_ch < b_ch:
            return -1
        if a_ch > b_ch:
            return 1
    if len(a) < len(b):
        return -1
    elif len(b) < len(a):
        return 1
    return 0


first_col_list = sorted(list(last_col_str), key=functools.cmp_to_key(cmp))
first_col = ''.join(first_col_list)
print(first_col)


# STEP3: Use the first-last property to recreate the first row
#   [$ ,t ,w ,e2,l2,v ,e3,p ,l1,u ,s ,o ,n ,e1]
#   [e1,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,n ]
#   [e2,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,w ]
#   [e3,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,v ]
#   [l1,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,p ]
#   [l2,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,e2]
#   [n ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,o ]
#   [o ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,s ]
#   [p ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,e3]
#   [s ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,u ]
#   [t ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,$ ]
#   [u ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,l1]
#   [v ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,l2]
#   [w ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,t ]

first_row = '$twelveplusone'


# #STEP4: Recall that the first row of the matrix is the FIRST rotation, so you need to rotate it backwards to get the
# original string ($ should be at the end, so rotate left)

original_val = next(rotate_left(first_row))
print(original_val)


