from collections import Counter
from typing import Dict, Tuple

from graph.Graph import Graph
from helpers.Utils import slide_window, unique_id_generator

# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.

#
# Load scoring matrix
#
opening_gap_penalty = -11  # specified in problem statement
closing_gap_penalty = 0    # implied
extended_gap_penalty = -1  # specified in problem statement
mismatch_penalties: Dict[Tuple[str, str], int] = {}
with open('BLOSUM62.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = data.strip().split('\n')
aa_row = lines[0].strip().split()
for line in lines[1:]:
    vals = line.strip().split()
    aa2 = vals[0]
    weight = vals[1:]
    for aa1, weight in zip(aa_row, weight):
        mismatch_penalties[(aa1, aa2)] = int(weight)


#
# Load sequences
#
with open('/home/user/Downloads/dataset_240307_8.txt', mode='r', encoding='utf-8') as f:
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


create_node_id = unique_id_generator('N')
create_edge_id = unique_id_generator('E')
g = Graph()
grid = {}
grid_rows = len(s1) + 1
grid_cols = len(s2) + 1
for layer_name in ['low', 'mid', 'up']:
    layer = []
    for i, s1_ch in enumerate([None] + s1):
        row = []
        for j, s2_ch in enumerate([None] + s2):
            node_id = f'{layer_name}{i}x{j}'
            row.append(node_id)
            g.insert_node(
                node_id,
                [None, None, s1_ch, s2_ch]
            )
        layer.append(row)
    grid[layer_name] = layer
for row_pair, _ in slide_window(grid['mid'], 2):  # create diagonal edges in mid-layer
    row1, row2 = row_pair
    for src_n, dst_n in zip(row1[:-1], row2[1:]):
        _, _, dst_n_s1_ch, dst_n_s2_ch = g.get_node_data(dst_n)
        penalty = mismatch_penalties[(dst_n_s1_ch, dst_n_s2_ch)]
        g.insert_edge(
            create_edge_id(),
            src_n,
            dst_n,
            [ModificationType.KEEP_BOTH, penalty]
        )
for (row1, row2), _ in slide_window(grid['low'], 2):  # create vertical edges in low-layer (extended gap penalties)
    for src_n, dst_n in zip(row1, row2):
        g.insert_edge(
            create_edge_id(),
            src_n,
            dst_n,
            [ModificationType.KEEP_S1_ONLY, extended_gap_penalty]
        )
for mid_row, low_row in zip(grid['mid'][:-1], grid['low'][1:]):  # ADD EDGES FROM MID TO LOW (opening gap penalty)
    for src_n, dst_n in zip(mid_row, low_row):
        g.insert_edge(
            create_edge_id(),
            src_n,
            dst_n,
            [ModificationType.KEEP_S1_ONLY, opening_gap_penalty]
        )
for low_row, mid_row in zip(grid['low'][1:], grid['mid'][1:]):  # ADD EDGES FROM LOW TO MID (closing gap penalty)
    for src_n, dst_n in zip(low_row, mid_row):
        g.insert_edge(
            create_edge_id(),
            src_n,
            dst_n,
            [ModificationType.SKIP, closing_gap_penalty]
        )
for row in grid['up']:  # create horizontal edges in up-layer (extended gap penalties)
    for (src_n, dst_n), _ in slide_window(row, 2):
        g.insert_edge(
            create_edge_id(),
            src_n,
            dst_n,
            [ModificationType.KEEP_S2_ONLY, extended_gap_penalty]
        )
for mid_row, up_row in zip(grid['mid'], grid['up']):  # ADD EDGES FROM MID TO UP (opening gap penalty)
    for src_n, dst_n in zip(mid_row[:-1], up_row[1:]):
        g.insert_edge(
            create_edge_id(),
            src_n,
            dst_n,
            [ModificationType.KEEP_S2_ONLY, opening_gap_penalty]
        )
for up_row, mid_row in zip(grid['up'], grid['mid']):  # ADD EDGES FROM UP TO MID (closing gap penalty)
    for src_n, dst_n in zip(up_row[1:], mid_row[1:]):
        g.insert_edge(
            create_edge_id(),
            src_n,
            dst_n,
            [ModificationType.SKIP, closing_gap_penalty]
        )
from_node = grid['mid'][0][0]  # middle layer top left
to_node = grid['mid'][-1][-1]  # middle layer bottom right


# Populate node weights and backtracking info. Each node's data is a tuple where [0] is the calculated weight and [1] is
# the edge the incoming connection that was chosen to calculate that weight (used for backtracking).
#
# from_node should be a root node. Initialize its weight to 0, but initialize all other root node weights to None.
# A None weight is used as a marker to skip over these because we don't want to consider them.
complete_nodes = set()
for node in g.get_nodes():  # Add all roots with None weight and None backtracking edge.
    if g.get_in_degree(node) == 0:
        initial_weight = None
        initial_backtrack = None
        node_data = g.get_node_data(node)
        node_data[0] = initial_weight
        node_data[1] = initial_backtrack
        complete_nodes |= {node}
waiting_nodes = set()
for node in complete_nodes:
    for e in g.get_outputs(node):
        dst_node = g.get_edge_to(e)
        if {g.get_edge_from(e) for e in g.get_inputs(dst_node)}.issubset(complete_nodes):
            waiting_nodes |= {dst_node}
# Overwrite start_node root with 0 weight
assert from_node in complete_nodes
from_node_data = g.get_node_data(from_node)
from_node_data[0] = 0
# Run the algorithm, populating node weights and backtracking edges
remaining_unprocessed_inputs_for_each_node = Counter()
for node in g.get_nodes():
    incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
    incoming_nodes -= complete_nodes
    remaining_unprocessed_inputs_for_each_node[node] = len(incoming_nodes)
while len(waiting_nodes) > 0:
    node = next(iter(waiting_nodes))
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
