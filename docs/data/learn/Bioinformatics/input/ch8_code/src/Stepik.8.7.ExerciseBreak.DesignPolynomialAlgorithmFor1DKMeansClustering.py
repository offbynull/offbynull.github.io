from statistics import mean

from helpers.Utils import slide_window

# Exercise Break: We have already stated that the k-Means Clustering Problem is NP-hard for k > 1. However, in the case
# of clustering in one-dimensional space (i.e., when all data points fall on a line), the k-Means Clustering Problem can
# be solved in polynomial time for any value of k. Design an algorithm for solving the k-Means Clustering Problem in
# this case.

# MY ANSWER
# ---------
# I tried to reason about this but I couldn't do it. I already know its wrong because for k=1, it should be equaling
# 20.5714... but it's actually giving back 26.5. Maybe step back and do it like this...
#
# for an example set of 2 points, bruteforce an answer for k=1 and k=2  (should be obvious)
# for an example set of 3 points, bruteforce an answer for k=1, k=2, and k=3
# for an example set of 4 points, bruteforce an answer for k=1, k=2, k=3, and k=4
#
# Then try to reverse engineer form the answers. That's probably not how it wants you to do it but this is so confusing.


# ---A---B-C---------D----E-----------F--G----
pts = [
    4.0,
    8.0,
    10.0,
    20.0,
    25.0,
    37.0,
    40.0
]
k = 1
pts = sorted(pts)
pts_len = len(pts)

centers = []
if k == 1:
    centers.append(mean(pts))
else:
    centers = pts.copy()
    while len(centers) > k:
        dists = [(p2 - p1)**2 / 2 for (p1, p2), _ in slide_window(centers, k=2)]
        min_dist = min(dists)
        min_dist_idx = dists.index(min_dist)
        avg = mean(centers[min_dist_idx:min_dist_idx + 2])
        del centers[min_dist_idx:min_dist_idx + 2]
        centers.insert(min_dist_idx, avg)

print(f'{centers=}')