from statistics import mean

from helpers.GeometryUtils import distance

# We can now formulate a well-defined clustering problem.
#
# k-Center Clustering Problem: Given a set of data points, find k centers minimizing the maximum distance between these
# data points and centers.
#
#     Input: A set of points Data and an integer k.
#     Output: A set Centers of k centers that minimize the distance MaxDistance(DataPoints, Centers) over all possible
#             choices of k centers.
#
# Exercise Break: How would you select a center in the case of only a single cluster (i.e., when k = 1)?

# MY ANSWER
# ---------
# My guess is that you can just average the x's to get the center x and average the y's to get the center y
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
    (mean(x for _, (x, _) in points), mean(y for _, (_, y) in points))
]

# THE CODE BELOW IS THE SAME CODE FROM THE PREVIOUS CODE CHALLENGE IN 8.5

# Get distance to closest center for each point
dist_to_closest_center = {}
for p_id, (x, y) in points:
    min_dist = min(distance(x, cx, y, cy) for cx, cy in centers)
    dist_to_closest_center[p_id] = min_dist

# Find the farthest distance from the calculation above
farthest_dist_to_closest_center = max(v for v in dist_to_closest_center.values())

print(f'{farthest_dist_to_closest_center}')
