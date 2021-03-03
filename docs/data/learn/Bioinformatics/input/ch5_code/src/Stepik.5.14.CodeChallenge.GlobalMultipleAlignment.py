import itertools

from graph.Graph import Graph

# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.

#
# Load scoring matrix
#
mismatch_or_indel_penalty = 0  # specified in problem statement
match_penalty = 1              # specified in problem statement


#
# Load sequences
#
with open('/home/user/Downloads/dataset_240309_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')

s1 = list(lines[0].strip())
s2 = list(lines[1].strip())
s3 = list(lines[2].strip())


#
# Generate graph
#
next_edge_id = 0
g = Graph()
grid = []
grid_rows = len(s1) + 1
grid_cols = len(s2) + 1
for x, s1_ch in enumerate([None] + s1):  # create nodes
    matrix = []
    for y, s2_ch in enumerate([None] + s2):
        row = []
        for z, s3_ch in enumerate([None] + s3):
            node_id = (x, y, z)
            row.append(node_id)
            g.insert_node(node_id, [None, None, s1_ch, s2_ch, s3_ch])
        matrix.append(row)
    grid.append(matrix)
for x, y, z in g.get_nodes():
    for x_offset, y_offset, z_offset in itertools.product([0, 1], repeat=3):
        if (x_offset, y_offset, z_offset) == (0, 0, 0):  # skip this or else you'll be making a connection to yourself
            continue
        src_n = (x, y, z)
        dst_n = (x + x_offset, y + y_offset, z + z_offset)
        if not g.has_node(dst_n):  # skip if the neighbouring node doesn't exist
            continue
        mod_type = (x_offset, y_offset, z_offset)
        symbols = g.get_node_data(dst_n)[2:]
        if mod_type == (1, 1, 1) and len(set(symbols)) == 1:  # if 3d diagonal edge (e.g. 0,0,0 to 1,1,1) and all same char, its a match
            penalty = match_penalty
        else:
            penalty = mismatch_or_indel_penalty
        g.insert_edge(next_edge_id, src_n, dst_n, [mod_type, penalty])
        next_edge_id += 1
from_node = grid[0][0][0]
to_node = grid[-1][-1][-1]


### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER
### README: WHEN ABSTRACTING TO A FUNCTION -- USE THE LOCAL ALIGNMENT VERSION AS IT HAS SOME OPTIMIZATIONS THAT MAKE IT RUN FASTER

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
        waiting_nodes |= {g.get_edge_to(e) for e in g.get_outputs(node)}
        complete_nodes |= {node}
# Overwrite start_node root with 0 weight
from_node_data = g.get_node_data(from_node)
from_node_data[0] = 0
# Run the algorithm, populating node weights and backtracking edges
while len(waiting_nodes) > 0:
    for node in waiting_nodes:
        incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
        if not incoming_nodes.issubset(complete_nodes):
            continue
        incoming_accum_weights = {}
        for edge in g.get_inputs(node):
            src_node = g.get_edge_from(edge)
            src_node_weight, _, _, _, _ = g.get_node_data(src_node)
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
            output_node_sources = {g.get_edge_from(e) for e in g.get_inputs(output_node)}
            if output_node_sources.issubset(complete_nodes):
                waiting_nodes.add(output_node)
        break

# Now backtrack from the end_node to start_node to get the path.
longest_path_length, _, _, _, _ = g.get_node_data(to_node)
longest_path_operations = [[None, to_node]]
_, backtracking_edge, _, _, _ = g.get_node_data(to_node)
while backtracking_edge is not None:
    prev_node, _, edge_data = g.get_edge(backtracking_edge)
    longest_path_operations[0][0] = edge_data[0]
    longest_path_operations.insert(0, [None, prev_node])
    _, backtracking_edge, _, _, _ = g.get_node_data(prev_node)


print(f'{longest_path_operations}')
# print(f'{g}')

s1_alignment = []
s1_idx = 0
s2_alignment = []
s2_idx = 0
s3_alignment = []
s3_idx = 0
for op, _ in longest_path_operations[1:]:
    if op[0] == 0:
        s1_alignment.append('-')
    elif op[0] == 1:
        s1_alignment.append(s1[s1_idx])
        s1_idx += 1

    if op[1] == 0:
        s2_alignment.append('-')
    elif op[1] == 1:
        s2_alignment.append(s2[s2_idx])
        s2_idx += 1

    if op[2] == 0:
        s3_alignment.append('-')
    elif op[2] == 1:
        s3_alignment.append(s3[s3_idx])
        s3_idx += 1


print(f'{longest_path_length}')
print(f'{"".join(s1_alignment)}')
print(f'{"".join(s2_alignment)}')
print(f'{"".join(s3_alignment)}')
