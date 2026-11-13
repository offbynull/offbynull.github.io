from helpers.GeometryUtils import distance

# Compute MaxDistance(Data, Centers) for Data shown in the figure below and Centers (2, 4), (6, 7), and (7, 3).
points = [
    ('A', (1.0, 6.0)),
    ('B', (1.0, 3.0)),
    ('C', (3.0, 4.0)),
    ('D', (5.0, 6.0)),
    ('E', (5.0, 2.0)),
    ('F', (7.0, 1.0)),
    ('G', (8.0, 7.0)),
    ('H', (10.0, 3.0)),
]

centers = [
    (2.0, 4.0),
    (6.0, 7.0),
    (7.0, 3.0),
]

# Get distance to closest center for each point
dist_to_closest_center = {}
for p_id, (x, y) in points:
    min_dist = min(distance(x, cx, y, cy) for cx, cy in centers)
    dist_to_closest_center[p_id] = min_dist

# Find the farthest distance from the calculation above
farthest_dist_to_closest_center = max(v for v in dist_to_closest_center.values())

print(f'{farthest_dist_to_closest_center}')
