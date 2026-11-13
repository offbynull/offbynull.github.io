from itertools import product
from math import dist
from statistics import mean

from helpers.Utils import slide_window

# Exercise Break: We have already stated that the k-Means Clustering Problem is NP-hard for k > 1. However, in the case
# of clustering in one-dimensional space (i.e., when all data points fall on a line), the k-Means Clustering Problem can
# be solved in polynomial time for any value of k. Design an algorithm for solving the k-Means Clustering Problem in
# this case.

# MY ANSWER
# ---------
# This was my last attempt. I'd initially tried to reason about this but couldn't. Then I came to this approach, which
# is me bruteforce approximating answers and trying to work backwards to an algorithm. It almost works. It seems the
# cases where it might fail are those where equidistant gaps are involved.
#
# I don't care enough to try and fix it. I've already wasted several days on this.
def find_closest_center(data_pt, center_pts):
    center_pt = min(
        center_pts,
        key=lambda cp: dist(data_pt, cp)
    )
    return center_pt, dist(center_pt, data_pt)


def squared_error_distortion(data_pts, center_pts):
    res = []
    for data_pt in data_pts:
        closest_center_pt, dist_to = find_closest_center(data_pt, center_pts)
        res.append(dist_to ** 2)
    return sum(res) / len(res)


center_pts_count = 3  # FAILS TO GET THE CORRECT ANSWER IF YOU SET THIS TO 2
data_pts = sorted([1.0, 3.0, 4.0, 5.0, 7.0])
min_data_pt = min(data_pts)
max_data_pt = max(data_pts)
step = (max_data_pt - min_data_pt) / 100.0
steps = []
curr_step = min_data_pt
while curr_step <= max_data_pt:
    steps.append(curr_step)
    curr_step += step
approximate_min_centers = None
for steps in product(steps, repeat=center_pts_count):
    steps = [(c,) for c in steps]
    sed = squared_error_distortion([(pt,) for pt in data_pts], steps)
    if approximate_min_centers is None:
        approximate_min_centers = steps, sed
    elif sed < approximate_min_centers[1]:
        approximate_min_centers = steps, sed
print(f'{approximate_min_centers=}')


def sort_by_widest_gap(sorted_data_pts):
    dists = {}
    for i, pt in enumerate(sorted_data_pts):
        gaps = []
        if i > 0:
            gaps.append((data_pts[i-1], pt))
        if i < len(data_pts) - 1:
            gaps.append((data_pts[i+1], pt))
        gaps.sort(reverse=True)
        pt1, pt2 = sorted(gaps[0])
        dists[pt1, pt2] = abs(pt2 - pt1)
    return sorted(((v, k) for k, v in dists.items()), reverse=True)


widest_gaps = sort_by_widest_gap(data_pts)[:center_pts_count-1]
print(f'{widest_gaps=}')
widest_gaps_split_markers = sorted([data_pts.index(v) for _, (v, _) in widest_gaps] + [len(data_pts) - 1])
print(f'{widest_gaps_split_markers=}')
split_data_pts = []
split_last_idx = 0
for idx in widest_gaps_split_markers:
    x = data_pts[split_last_idx:idx + 1]
    split_data_pts.append(x)
    split_last_idx = idx + 1
print(f'{split_data_pts=}')
algorithm_min_centers = [mean(x) for x in split_data_pts]
print(f'{algorithm_min_centers=}')
print()
print(f'The best k-means {center_pts_count} center points for {data_pts} ')
print(f'Approximated     = {[x[0] for x in approximate_min_centers[0]]}')
print(f'Approximated SED = {approximate_min_centers[1]}')
print(f'Algorithm        = {algorithm_min_centers}')
print(f'Algorithm SED    = {squared_error_distortion([(x,) for x in data_pts], [(x,) for x in algorithm_min_centers])}')

