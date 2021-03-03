from collections import Counter
from itertools import product
from typing import Dict, Tuple

from graph.Graph import Graph
from helpers.Utils import slide_window

# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.

#
# Load scoring matrix
#
indel_penalty = -1  # specified in problem statement
mismatch_penalties: Dict[Tuple[str, str], int] = {}
for ch1, ch2 in product('ACTG', repeat=2):
    mismatch_penalties[(ch1, ch2)] = 1 if ch1 == ch2 else -1


#
# Load sequences
#
with open('/home/user/Downloads/dataset_240306_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')

s1 = list(lines[0].strip())
s2 = list(lines[1].strip())


#
# Generate graph
#
class ModificationType:
    KEEP_S1_ONLY = 'KEEP_S1_ONLY'
    KEEP_S2_ONLY = 'KEEP_S2_ONLY'
    KEEP_BOTH = 'KEEP_BOTH'
    SKIP = 'SKIP'


next_edge_id = 0
next_node_id = 0
g = Graph()
grid = []
grid_rows = len(s1) + 1
grid_cols = len(s2) + 1
for s1_ch in [None] + s1:  # create nodes
    row = []
    for s2_ch in [None] + s2:
        node_id = next_node_id
        next_node_id += 1
        row.append(node_id)
        g.insert_node(node_id, [None, None, s1_ch, s2_ch])
    grid.append(row)
for row in grid:  # create horizontal edges
    for node_pair, _ in slide_window(row, 2):
        src_n, dst_n = node_pair
        g.insert_edge(next_edge_id, src_n, dst_n, [ModificationType.KEEP_S2_ONLY, indel_penalty])
        next_edge_id += 1
for row_pair, _ in slide_window(grid, 2):  # create vertical edges
    row1, row2 = row_pair
    for src_n, dst_n in zip(row1, row2):
        g.insert_edge(next_edge_id, src_n, dst_n, [ModificationType.KEEP_S1_ONLY, indel_penalty])
        next_edge_id += 1
for row_pair, _ in slide_window(grid, 2):  # create diagonal edges
    row1, row2 = row_pair
    for src_n, dst_n in zip(row1[:-1], row2[1:]):
        _, _, dst_n_s1_ch, dst_n_s2_ch = g.get_node_data(dst_n)
        penalty = mismatch_penalties[(dst_n_s1_ch, dst_n_s2_ch)]
        g.insert_edge(next_edge_id, src_n, dst_n, [ModificationType.KEEP_BOTH, penalty])
        next_edge_id += 1
from_node = grid[0][0]
to_node = grid[-1][-1]
for row in grid:  # create free-rides from source node to every node in the first column
    dst_n = row[0]
    if dst_n == from_node:
        continue
    g.insert_edge(next_edge_id, from_node, dst_n, [ModificationType.SKIP, 0])
    next_edge_id += 1
for row in grid:  # create free-rides from every node in the last column to dst node
    src_n = row[-1]
    if src_n == to_node:
        continue
    g.insert_edge(next_edge_id, src_n, to_node, [ModificationType.SKIP, 0])
    next_edge_id += 1

# Populate node weights and backtracking info. Each node's data is a tuple where [0] is the calculated weight and [1] is
# the edge the incoming connection that was chosen to calculate that weight (used for backtracking).
#
# from_node should be a root node. Initialize its weight to 0, but initialize all other root node weights to None.
# A None weight is used as a marker to skip over these because we don't want to consider them.
waiting_nodes = set()
complete_nodes = set()
for node in g.get_nodes():  # Add all roots with None weight and None backtracking edge.
    if g.get_in_degree(node) == 0:
        initial_weight = None
        initial_backtrack = None
        node_data = g.get_node_data(node)
        node_data[0] = initial_weight
        node_data[1] = initial_backtrack
        for e in g.get_outputs(node):
            dst_node = g.get_edge_to(e)
            if {node} == {g.get_edge_from(e) for e in g.get_inputs(dst_node)}:
                waiting_nodes |= {dst_node}
        complete_nodes |= {node}
# Overwrite start_node root with 0 weight
from_node_data = g.get_node_data(from_node)
from_node_data[0] = 0
# Run the algorithm, populating node weights and backtracking edges
remaining_unprocessed_inputs_for_each_node = Counter()
for node in g.get_nodes():
    incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
    incoming_nodes.discard(from_node)
    remaining_unprocessed_inputs_for_each_node[node] = len(incoming_nodes)
while len(waiting_nodes) > 0:
    for node in waiting_nodes:
        incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
        if not incoming_nodes.issubset(complete_nodes):
            continue
        incoming_accum_weights = {}
        for edge in g.get_inputs(node):
            src_node = g.get_edge_from(edge)
            src_node_weight, _, _, _ = g.get_node_data(src_node)
            _, edge_weight = g.get_edge_data(edge)
            # Roots that aren't from_node were initialized to a weight of None -- if you see them, skip them.
            if src_node_weight is not None:
                incoming_accum_weights[edge] = src_node_weight + edge_weight
        if len(incoming_accum_weights) == 0:
            max_edge = None
            max_weight = None
        else:
            max_edge = max(incoming_accum_weights, key=lambda e: incoming_accum_weights[e])
            max_weight = incoming_accum_weights[max_edge]
        node_data = g.get_node_data(node)
        node_data[0] = max_weight
        node_data[1] = max_edge
        # This node has been processed, move it over to complete_nodes.
        waiting_nodes.remove(node)
        complete_nodes.add(node)
        # For outgoing nodes this node points to, if that outgoing node has all of its dependencies in complete_nodes,
        # then add it to waiting_nodes (so it can be processed).
        outgoing_nodes = {g.get_edge_to(e) for e in g.get_outputs(node)}
        for output_node in outgoing_nodes:
            remaining_unprocessed_inputs_for_each_node[output_node] -= 1
            if remaining_unprocessed_inputs_for_each_node[output_node] == 0:
                waiting_nodes.add(output_node)
        break

# Now backtrack from the end_node to start_node to get the path.
longest_path_length, _, _, _ = g.get_node_data(to_node)
longest_path_operations = [[None, to_node]]
_, backtracking_edge, _, _ = g.get_node_data(to_node)
while backtracking_edge is not None:
    prev_node, _, edge_data = g.get_edge(backtracking_edge)
    longest_path_operations[0][0] = edge_data[0]
    longest_path_operations.insert(0, [None, prev_node])
    _, backtracking_edge, _, _ = g.get_node_data(prev_node)


# print(f'{longest_path_operations}')
# print(f'{g}')

s1_alignment = []
s2_alignment = []
for op, node in longest_path_operations[1:]:
    if op == ModificationType.KEEP_S1_ONLY:
        _, _, s1_ch, s2_ch = g.get_node_data(node)
        s1_alignment.append(s1_ch)
        s2_alignment.append('-')
    elif op == ModificationType.KEEP_S2_ONLY:
        _, _, s1_ch, s2_ch = g.get_node_data(node)
        s1_alignment.append('-')
        s2_alignment.append(s2_ch)
    elif op == ModificationType.KEEP_BOTH:
        _, _, s1_ch, s2_ch = g.get_node_data(node)
        s1_alignment.append(s1_ch)
        s2_alignment.append(s2_ch)
    elif op == ModificationType.SKIP:
        continue  # do nothing -- this is a free ride to the starting point


print(f'{longest_path_length}')
print(f'{"".join(s1_alignment)}')
print(f'{"".join(s2_alignment)}')
