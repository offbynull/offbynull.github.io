import re

from graph.Graph import Graph

# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.

with open('/home/user/Downloads/dataset_240303_7.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')

start_node = int(lines[0].strip())
end_node = int(lines[1].strip())

g = Graph()
next_e_id = 0
for l in lines[2:]:
    in_node, out_node, edge_weight = [int(v) for v in re.split('->|:', l)]
    if not g.has_node(in_node):
        g.insert_node(in_node)
    if not g.has_node(out_node):
        g.insert_node(out_node)
    g.insert_edge(f'E{next_e_id}', in_node, out_node, edge_weight)
    next_e_id += 1


# Populate node weights and backtracking info. Each node's data is a tuple where [0] is the calculated weight and [1] is
# the edge the incoming connection that was chosen to calculate that weight (used for backtracking).
#
# start_node should be a root node. Initialize its weight to 0, but initialize all other root node weights to None.
# A None weight is used as a marker to skip over these because we don't want to consider them.
check_nodes = set()
ready_nodes = set()
for node in g.get_nodes():  # Add all roots with None weight and None backtracking edge.
    if g.get_in_degree(node) == 0:
        initial_weight = None
        g.update_node_data(node, (initial_weight, None))
        check_nodes |= {g.get_edge_to(e) for e in g.get_outputs(node)}
        ready_nodes |= {node}
g.update_node_data(start_node, (0, None))  # Overwrite start_node root with 0 weight and None backtracking edge
# Run the algorithm, populating node weights and backtracking edges
while len(check_nodes) > 0:
    for node in check_nodes:
        incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
        if incoming_nodes.issubset(ready_nodes):
            incoming_accum_weights = {}
            for edge in g.get_inputs(node):
                source_node = g.get_edge_from(edge)
                source_node_weight, _ = g.get_node_data(source_node)
                edge_weight = g.get_edge_data(edge)
                # Roots that aren't start_node were initialized to a weight of None -- if you see them, skip them.
                if source_node_weight is not None:
                    incoming_accum_weights[edge] = source_node_weight + edge_weight
            if len(incoming_accum_weights) == 0:
                max_edge = None
                max_weight = None
            else:
                max_edge = max(incoming_accum_weights, key=lambda e: incoming_accum_weights[e])
                max_weight = incoming_accum_weights[max_edge]
            g.update_node_data(node, (max_weight, max_edge))
            check_nodes.remove(node)
            check_nodes |= {g.get_edge_to(e) for e in g.get_outputs(node)}
            ready_nodes |= {node}
            break

# Now backtrack from the end_node to start_node to get the path.
longest_path_length, _ = g.get_node_data(end_node)
longest_path = [end_node]
_, backtracking_edge = g.get_node_data(end_node)
while backtracking_edge is not None:
    prev_node = g.get_edge_from(backtracking_edge)
    longest_path.insert(0, prev_node)
    _, backtracking_edge = g.get_node_data(prev_node)

print(f'{longest_path_length}')
print(f'{"->".join([str(n) for n in longest_path])}')
