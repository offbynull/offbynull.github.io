from collections import defaultdict
from math import dist, nan
from statistics import mean

with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = [s.strip() for s in data.strip().split('\n')]

num_centers, dims = [int(e) for e in lines[0].split()]
points = []
for l in lines[1:]:
    pt = tuple(float(n) for n in l.split())
    points.append(pt)


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
centers = points[:num_centers]
while centers != old_centers:
    print(f'{centers}')
    mapping = defaultdict(list)
    for pt in points:
        ct_pt, _ = find_closest_center(pt, centers)
        mapping[ct_pt].append(pt)
    old_centers = centers
    centers = [nan] * num_centers
    for i, pts in enumerate(mapping.values()):
        centers[i] = tuple(center_of_gravity(pts, dims))
for ct in centers:
    line = ' '.join(f'{coord:.3f}' for coord in ct)
    print(line)
