# EXERCISE BREAK
#
# The algorithm proposed on the previous step computes LimbLength(j) in O(n^2) time (for an n x n distance matrix).
# Design an algorithm that computes LimbLength(j) in O(n) time.


# For reference, this is the non-linear algorithm...
#
# min_limb_len = None
# for i, k in product(range(mat_size), range(mat_size)):
#     if i == leaf_idx or k == leaf_idx:
#         continue
#     limb_len = (dist_mat[i][leaf_idx] + dist_mat[k][leaf_idx] - dist_mat[i][k]) / 2
#     if min_limb_len is None or limb_len < min_limb_len:
#         min_limb_len = limb_len
# print(f'{int(min_limb_len)}')

# The algorithm above is (Di,j + Dj,k - Di,k) / 2
#
# Maybe the solution here is to limit the scope somehow? Maybe get the min Di,j and min Dj,k so that when you add them
# you get a small number, then hope that when you subtract Di,k it'll be the actual minimum?
#
# Maybe the solution here is to pair down the distance matrix? So instead of ...
#
#           vv
#     0     13    21    22
# >>  13    0     12    13
#     21    12    0     13
#     22    13    13     0
#
# ... you start with a sub-range...
#           vv
#     0     13    21
# >>  13    0     12
#     21    12    0
#
# .. and iteratively grow the bounds of the matrix either left/right or up/down based on the minimum you calculate? This
# is probably wrong.

# I don't have a good answer for this.
