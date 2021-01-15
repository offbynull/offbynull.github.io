# Populate node weights and backtracking info. Each node's data is a tuple where [0] is the calculated weight and [1] is
# the edge the incoming connection that was chosen to calculate that weight (used for backtracking).
#
# from_node should be a root node. Initialize its weight to 0, but initialize all other root node weights to None.
# A None weight is used as a marker to skip over these because we don't want to consider them.
from collections import Counter
from typing import TypeVar, Callable, Optional

from Graph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')

def populate_weights_and_backtrack_pointers(
        g: Graph[N, ND, E, ED],
        from_node: N,
        set_node_data_func: Callable[
            [
                N,                # node ID
                Optional[float],  # max weight of node
                E                 # edge ID of incoming edge made node have max weight
            ],
            None
        ]
):
    processed_nodes = set()          # nodes where all parents have been processed AND it has been processed
    waiting_nodes = set()            # nodes where all parents have been processed BUT it has yet to be processed
    unprocessable_nodes = Counter()  # nodes that have some parents are remaining are processed (value=# of parents left)
    # For all root nodes, add to processed_nodes and set None weight and None backtracking edge.
    for node in g.get_nodes():
        if g.get_in_degree(node) == 0:
            set_node_data_func(node, None, None)
            processed_nodes |= {node}
    # For all root nodes, add any children where its the only parent to waiting_nodes.
    for node in processed_nodes:
        for e in g.get_outputs(node):
            dst_node = g.get_edge_to(e)
            if {g.get_edge_from(e) for e in g.get_inputs(dst_node)}.issubset(processed_nodes):
                waiting_nodes |= {dst_node}
    # Make sure from_node is a root and set its weight to 0.
    assert from_node in processed_nodes
    set_node_data_func(from_node, 0.0, None)
    # Track how many remaining parents each node in the graph has. Note that the graph's root nodes were already marked
    # as processed above.
    for node in g.get_nodes():
        incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
        incoming_nodes -= processed_nodes
        unprocessable_nodes[node] = len(incoming_nodes)
    # Any nodes in waiting_nodes have had all their parents already processed (in processed_nodes). As such, they can
    # have their weights and backtracking pointers calculated. They can then be placed into processed_nodes themselves.
    while len(waiting_nodes) > 0:
        node = next(iter(waiting_nodes))
        incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
        if not incoming_nodes.issubset(processed_nodes):
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
        set_node_data_func(from_node, max_weight, max_edge)
        # This node has been processed, move it over to processed_nodes.
        waiting_nodes.remove(node)
        processed_nodes.add(node)
        # For outgoing nodes this node points to, if that outgoing node has all of its dependencies in processed_nodes,
        # then add it to waiting_nodes (so it can be processed).
        outgoing_nodes = {g.get_edge_to(e) for e in g.get_outputs(node)}
        for output_node in outgoing_nodes:
            unprocessable_nodes[output_node] -= 1
            if unprocessable_nodes[output_node] == 0:
                waiting_nodes.add(output_node)