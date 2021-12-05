from itertools import product
from typing import Iterable

# Exercise Break: Design a polynomial algorithm to check whether there is a solution of the Good Clustering Problem.
#
#

# MY ANSWER
# ---------
# "Polynomial time" is relation to input. If the input is a set of coordinates, I can't see how this is possible. If the
# input is the shortest possible distance for each node, then it seems like it's possible?
#
# Given a list of node pairs, for each pair a and b...
#   no closer node exists to b other than a
#   no closer node exists to a other than b
#
# Sort the list by distance (closest to farthest).
#
# Walk the sorted list from smallest dist to largest dist. For each pair, ...
#  if neither of the nodes are grouped, place them into the same group (cluster)
#  if one of the elements is already in a group, add the other to that group (cluster)
#  if both elements are already in groups, something's wrong
from helpers.GeometryUtils import distance

n = [
    ('A', (1.0, 6.0)),
    ('B', (1.0, 3.0)),
    ('C', (3.0, 4.0)),
    ('D', (5.0, 6.0)),
    ('E', (5.0, 2.0)),
    ('F', (7.0, 1.0)),
    ('G', (8.0, 7.0)),
    ('H', (10.0, 3.0)),
]

# for each node, find the other node that has the shortest possible distance
dists = {}
for a, (a_x, a_y) in n:
    found_dist = None
    for b, (b_x, b_y) in n:
        if a == b:
            continue
        dist = distance(a_x, b_x, a_y, b_y)
        if found_dist is None or dist < found_dist:
            found_b, (found_b_x, found_b_y) = b, (b_x, b_y)
            found_dist = dist
    n1, n2 = sorted([a, found_b])
    dists[n1, n2] = found_dist

# sort smallest to largest
sorted_dists = sorted((v, k) for k, v in dists.items())

# group until a conflict arises
#   having trouble reasoning about this? maybe visualize what's happening on a plot -- draw whats happening at each
#   iteration of the loop, coloring each line by the group its in (e.g. group 0 = red, group 1 = blue, etc..) -- it'll
#   become apparent what's happening.
node_to_group = {}
next_group_id = 0
while sorted_dists:
    dist, (a, b) = sorted_dists.pop()
    a_exists = a in node_to_group
    b_exists = b in node_to_group
    if a_exists and not b_exists:
        expected_group_id = node_to_group[a]
        node_to_group[b] = expected_group_id
    elif not a_exists and b_exists:
        expected_group_id = node_to_group[b]
        node_to_group[a] = expected_group_id
    elif not a_exists and not b_exists:
        node_to_group[a] = next_group_id
        node_to_group[b] = next_group_id
        next_group_id += 1
    else:
        raise ValueError(f'Next shortest distance is {dist} between {a, b}, but '
                         f'{a} has already been grouped with {node_to_group[a]} and '
                         f'{b} has already been grouped with {node_to_group[b]}')

print('Ok')
print(f'{node_to_group}')
