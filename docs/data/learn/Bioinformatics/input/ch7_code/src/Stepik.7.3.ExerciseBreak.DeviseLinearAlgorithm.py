# EXERCISE BREAK
#
# The algorithm proposed on the previous step computes LimbLength(j) in O(n^2) time (for an n x n distance matrix).
# Design an algorithm that computes LimbLength(j) in O(n) time.


# UPDATE: I figured this out, but it required a couple of days of futzing around and understanding the limb length
# algorithm. Block from notes below...
#
#    The answer to this is obvious now that I've gone through and reasoned about things above.
#
#    For the limb length formula to work, you need to find leaf nodes (A, B) whose path travels through leaf node L's
#    parent (Lp). Originally, the book had you try all combination of leafs (L excluded) and take the minimum. That
#    works, but you don't need to try all possible pairs. Instead, you can just pick any leaf (that isn't L) for A and
#    test against every other node (that isn't L) to find B -- as with the original method, you pick the B that produces
#    the minimum value.
#
#    Because a phylogenetic tree is a connected graph (a path exists between each node and all other nodes), at least 1
#    path will exist starting from A that travels through Lp.
#
#    ```python
#    leaf_nodes.remove(L)  # remove L from the set
#    A = leaf_nodes.pop()  # removes and returns an arbitrary leaf node
#    B = min(leafs, key=lambda x: (dist(L, A) + dist(L, x) - dist(A, x)) / 2)
#    ```
#
# To understand this better, read the section on limb length in the notes.
#
# For example, imagine that you're trying to find v2's limb length in the following graph...
#     v0
#       \
#    v1--i0              v6
#          \            /
#      v2---i1---i2---i3---v5
#          /       \
#        v3         v4
#
# Pick v4 as your A node, then try the formula with every other leaf node as B (except v2 because that's the node you're
# trying to get limb length for + v4 because that's your A node). At least one of path(A, B)'s will cross through v2's
# parent. Take the minimum, just as you did when you were trying every possible node pair across all leaf nodes in the
# graph.


# ATTEMPT BEFORE UPDATE ABOVE IS AS FOLLOWS:
#
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

# UPDATE: My second attempt at solving this problem:
#
#   a b f g z
# a 0 ? ? ? ?
# b ? 0 ? ? ?
# f ? ? 0 ? ?
# g ? ? ? 0 ?
# z ? ? ? ? 0
#
# This is the normal way of doing it (each pair of distances is tested)
#   Dd,z = min(
#     (Da,z + Db,z - Da,f) / 2,
#     (Da,z + Df,z - Da,f) / 2,
#     (Da,z + Dg,z - Da,g) / 2,
#     (Db,z + Df,z - Db,f) / 2,
#     (Db,z + Dg,z - Db,g) / 2,
#     (Df,z + Dg,z - Df,g) / 2
#   )
#
# The formula here is (D?,z + D?,z - D?,?) / 2. Instead of doing the above...
#   Take z's row and sort ascending by D?,z + D?,z
#   Calculate for the 2 values at idx0 in sorted row
#   Calculate for the 2 values at idx1 in sorted row, stop if D?,? < prev result
#   Calculate for the 2 values at idx2 in sorted row, stop if D?,? < prev result
#   ...
#
# The algorithm above is wrong but it has to be something like that. You're not touching every element of the matrix but
# sorting the matrix row means that it's no longer O(n), so I don't know for sure. I'll have to look into this more
# later.
#
# The following code block seems to be working with the two test data sets I have, but I don't know if that's just a
# coincidence or if there's some logic here that I'm not able to suss out...
#
# target = sorted(enumerate(dist_mat[leaf_idx]), key=lambda x: x[1])
# target.remove((leaf_idx, 0))
# for ((i1, v1), (i2, v2)), _ in slide_window(target, k=2):
#     limb_len = (dist_mat[i1][leaf_idx] + dist_mat[i2][leaf_idx] - dist_mat[i1][i2]) / 2
#     if min_limb_len is None or limb_len < min_limb_len:
#         min_limb_len = limb_len
#     elif limb_len > min_limb_len:
#         break
# print(f'{int(min_limb_len)}')
