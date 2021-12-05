from math import dist

with open('/home/user/Downloads/dataset_240359_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = [s.strip() for s in data.strip().split('\n')]

num_centers, dims = [int(e) for e in lines.pop(0).split()]
centers = []
while (l := lines.pop(0)):
    if l == '--------':
        break
    pt = tuple(float(n) for n in l.split())
    centers.append(pt)
points = []
while lines and (l := lines.pop(0)):
    pt = tuple(float(n) for n in l.split())
    points.append(pt)


def distortion(points, centers):
    # Get distance to closest center for each point
    dist_to_closest_center = []
    for p in points:
        min_dist = min(dist(p, c) for c in centers)
        dist_to_closest_center.append(min_dist)
    # sum square and mean
    return sum(x**2 for x in dist_to_closest_center) / len(points)


print(f'{distortion(points, centers):.3f}')

