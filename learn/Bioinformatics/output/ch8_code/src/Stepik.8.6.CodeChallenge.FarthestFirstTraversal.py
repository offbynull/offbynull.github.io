from math import dist

with open('/home/user/Downloads/dataset_240358_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = [s.strip() for s in data.strip().split('\n')]

num_centers, dims = [int(e) for e in lines[0].split()]
points = []
for l in lines[1:]:
    pt = tuple(float(n) for n in l.split())
    points.append(pt)

centers = [
    points[0]
]

while len(centers) < num_centers:
    dist_to_closest_center = {}
    for pt in points:
        min_dist = min(dist(pt, c_pt) for c_pt in centers)
        dist_to_closest_center[pt] = min_dist
    farthest_pt_to_closest_center = max(dist_to_closest_center, key=lambda x: dist_to_closest_center[x])
    centers.append(farthest_pt_to_closest_center)

for c_pt in centers:
    print(" ".join(str(n) for n in c_pt))
