from helpers.GeometryUtils import distance


# Exercise Break: Compute the values of MaxDistance(Data, Centers) and Distortion(Data, Centers) for the eight data
# points in the figure below and the three centers (3, 4.5), (6, 1.5), and (9, 5). How do these values differ if the
# centers are instead (5/3, 13/3), (6.5, 6.5), and (22/3, 2)?

# MY ANSWER (produced using code below)
# ---------
# FOR FIRST CENTERS:
#   max_distance(points, centers)=2.5
#   distortion(points, centers)=3.9375
# FOR SECOND CENTERS:
#   max_distance(points, centers)=2.8480012484391772
#   distortion(points, centers)=3.375
#
# The worse that the centers are, the lower the distortion is? I don't know.

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


def max_distance(points, centers):
    # Get distance to closest center for each point
    dist_to_closest_center = {}
    for p_id, (x, y) in points:
        min_dist = min(distance(x, cx, y, cy) for cx, cy in centers)
        dist_to_closest_center[p_id] = min_dist
    # Find the farthest distance from the calculation above
    return max(v for v in dist_to_closest_center.values())


def distortion(points, centers):
    # Get distance to closest center for each point
    dist_to_closest_center = {}
    for p_id, (x, y) in points:
        min_dist = min(distance(x, cx, y, cy) for cx, cy in centers)
        dist_to_closest_center[p_id] = min_dist
    # sum square and mean
    return sum(x**2 for x in dist_to_closest_center.values()) / len(points)

centers = [(3.0, 4.5), (6.0, 1.5), (9.0, 5.0)]
print(f'{max_distance(points, centers)=}')
print(f'{distortion(points, centers)=}')

centers = [(5/3, 13/3), (6.5, 6.5), (22/3, 2.0)]
print(f'{max_distance(points, centers)=}')
print(f'{distortion(points, centers)=}')