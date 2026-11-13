# EXERCISE BREAK
# --------------
# Exercise Break: Prove that if D is additive, then for any i and j between 1 and n, both (1/2)*(Di,j + Δi,j) and
# (1/2)*(Di,j - Δi,j) are non-negative.


# MY ATTEMPT AT ANSWERING
# -----------------------
# tot_dist = [sum(row) for row in dist_mat]
# for l1, l2 in product(range(n), range(n)):
#     neighbouring_join_mat[l1][l2] = (n-2) * dist_mat[l1][l2] - tot_dist[l1] - tot_dist[l2]
# Δi,j = (tot_dist[l1] - tot_dist[l2]) / (n-2)
#
#
# For calcing neighbouring_join_mat...
#  * tot_dist[i] has the dist sum of all paths to i
#  * tot_dist[j] has the dist sum of all paths to j
#  * (n-2) * dist_mat[i][j] is the dist sum of path (i, j) multiplied (n-2) times
# So what is this doing? Calculating how much "extra" dist sum there is vs what it would be if the dists used to
# calculate tot_dists[i] and tot_dists[j] were all exactly dist_mat[i][j]. It's multiplying by n-2 rather than n because
# each dist_row row/col has a 0 (dist to self). Something like that.
#
# For calcing Δi,j, it's essentially getting the average difference between the two sets of distances. That is, given
# all the distances for i and all the distances for j, get the average difference between thw two. It's dividing by n-2
# rather than n because each dist_row row/col has a 0 (dist to self).
#
# Prove that if D is additive, then for any i and j between 1 and n, both (1/2)*(Di,j + Δi,j) and (1/2)*(Di,j - Δi,j)
# are non-negative.
#
# * Δi,j = average difference between i's dists and j's dists
# * Di,j + Δi,j = the distance for (i,j) + average diff between i's dists and j's dists
# * Di,j - Δi,j = the distance for (i,j) - average diff between i's dists and j's dists
#
# If D is additive, a simple tree fits it and that tree doesn't have any negative edge weights. That means none of the
# paths used in calculating Δi,j contain negative edge weights, ultimately meaning that abs(Δi,j) is smaller than Di,j?

# That last part seems not right but close. I don't have the capacity / time to fully solve this. This seems like a good
# start as to what's happening (if you don't count the last paragraph).
