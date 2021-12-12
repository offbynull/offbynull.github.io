from collections import defaultdict
from math import dist, nan
from statistics import mean

num_centers, dims = 2, 1
points = [
    (0,),
    (1,),
    (1.9,),
    (3,)
]


def find_closest_center(data_pt, center_pts):
    center_pt = min(
        center_pts,
        key=lambda cp: dist(data_pt, cp)
    )
    return center_pt, dist(center_pt, data_pt)


def center_of_gravity(data_pts, dim):
    dim_means = []
    for i in range(dim):
        res = mean(data_pt[i] for data_pt in data_pts)
        dim_means.append(res)
    return dim_means


old_centers = []
centers = [(1,), (3,)]
while centers != old_centers:
    mapping = defaultdict(list)
    for pt in points:
        ct_pt, _ = find_closest_center(pt, centers)
        mapping[ct_pt].append(pt)
    old_centers = centers
    centers = [nan] * num_centers
    for i, pts in enumerate(mapping.values()):
        centers[i] = tuple(center_of_gravity(pts, dims))
    print(f'{list(zip(centers, mapping.values()))}')
for ct in centers:
    line = ' '.join(f'{coord:.3f}' for coord in ct)
    print(line)
