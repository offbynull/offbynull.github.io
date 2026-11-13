import math
from builtins import sorted
from collections import defaultdict
from itertools import product

from graph import DirectedGraph
from graph.GraphHelpers import StringIdGenerator

# Exercise Break: Solve the Most Likely Outcome Problem (Hint: You may need to build a 3-dimensional version of
# Viterbi’s Manhattan).

# MY ANSWER
# ---------
# This is the same thing as the code challenge, but the modified to support multiple "layers"/"grids". The source points
# to the starting column of all grids, and the ending column of all grids point to the sink node.
#
# THIS MIGHT NOT BE CORRECT. HERE'S WHAT YOU SHOULD DO: Bruteforce all possible sequences to see which one has the
# highest probability of occurring, then do it using this algorithm to see if it produces the same result.
symbols = {'x', 'y', 'z'}
hidden_states = {'A', 'B'}
hidden_state_transition_probs = {
    ('A', 'A'): 0.303,
    ('A', 'B'): 0.697,
    ('B', 'A'): 0.831,
    ('B', 'B'): 0.169
}
state_symbol_emission_probs = {
    ('A', 'x'): 0.401,
    ('A', 'y'): 0.400,
    ('A', 'z'): 0.402,
    ('B', 'x'): 0.333,
    ('B', 'y'): 0.334,
    ('B', 'z'): 0.332
}


class NodeData:
    def __init__(self, weight: float, backtrack_symbol: str | None):
        self.weight = weight
        self.backtrack_symbol = backtrack_symbol

    def __str__(self):
        return f'w={self.weight} backtrack_elem={self.backtrack_symbol}'

    def __format__(self, format_spec):
        return str(self)


class EdgeData:
    def __init__(self, weight: float):
        self.weight = weight

    def __str__(self):
        return f'{self.weight}'

    def __format__(self, format_spec):
        return str(self)


g = DirectedGraph.Graph()
g.insert_node('SOURCE', NodeData(1.0, None))
g.insert_node('SINK', NodeData(math.nan, None))
e_id_gen = StringIdGenerator('E')

n = 30

# Build graph with edge weights
for to_element_idx, to_hidden_state, to_emitted_symbol in product(range(n), hidden_states, symbols):
    g.insert_node(
        (to_element_idx, to_hidden_state, to_emitted_symbol),
        NodeData(math.nan, None)
    )
    if to_element_idx == 0:
        continue
    from_element_idx = to_element_idx - 1
    for from_hidden_state, from_emitted_symbol in product(hidden_states, symbols):
        g.insert_edge(
            next(e_id_gen),
            (from_element_idx, from_hidden_state, from_emitted_symbol),
            (to_element_idx, to_hidden_state, to_emitted_symbol),
            EdgeData(hidden_state_transition_probs[from_hidden_state, to_hidden_state])
        )
for to_hidden_state, to_emitted_symbol in product(hidden_states, symbols):
    g.insert_edge(
        next(e_id_gen),
        f'SOURCE',
        (0, to_hidden_state, to_emitted_symbol),
        EdgeData(1.0 / len(hidden_states))
    )
for from_hidden_state, from_emitted_symbol in product(hidden_states, symbols):
    g.insert_edge(
        next(e_id_gen),
        (n - 1, from_hidden_state, from_emitted_symbol),
        f'SINK',
        EdgeData(1.0)
    )


# Go through and assign node weights. For each node, group incoming edges by the "symbol" on the node they're coming
# from. Do the calculation on each group (symbol) and select the group with the highest weight before moving forward.
# This is doing the same type of "max edge" dynamic programming edge backtracking, but it's just aggregating edges
# together by symbol (you're backtracking to a set of edges as identified by their common symbol).
def aggregate_incoming_edges_by_symbol_and_select_max(n_id):
    # Get state-symbol emission probability
    if n_id != 'SINK':
        _, n_to_hidden_state, n_to_emitted_symbol = n_id
        to_state_symbol_emission_prob = state_symbol_emission_probs[n_to_hidden_state, n_to_emitted_symbol]
    else:
        to_state_symbol_emission_prob = 1.0
    # Add together edge weights, which are state-state transition probabilities (grouped by emitted symbol)
    n_weight_by_from_symbol = defaultdict(lambda: 0.0)
    for e_id in g.get_inputs(n_id):
        e_weight = g.get_edge_data(e_id).weight
        n_from_id = g.get_edge_from(e_id)
        n_from_weight = g.get_node_data(n_from_id).weight
        if n_from_id == 'SOURCE':
            n_weight_by_from_symbol[''] += n_from_weight * e_weight
        else:
            _, _, n_from_emitted_symbol = n_from_id
            n_weight_by_from_symbol[n_from_emitted_symbol] += n_from_weight * e_weight
    # Multiply by state-emission probability (grouped by emitted symbol)
    for n_from_emitted_symbol in n_weight_by_from_symbol:
        n_weight_by_from_symbol[n_from_emitted_symbol] *= to_state_symbol_emission_prob
    n_weight, n_backtrack_symbol = max((v, k) for k, v in n_weight_by_from_symbol.items())
    return n_weight, n_backtrack_symbol


# Dynamic programming "backtracking symbols", similar to backtracking edges.
ordered_node_ids = ['SOURCE'] + list(product(range(n), hidden_states, symbols)) + ['SINK']
for n_id in ordered_node_ids:
    if n_id in {'SOURCE'}:
        continue
    n_weight, n_backtrack_symbol = aggregate_incoming_edges_by_symbol_and_select_max(n_id)
    n_data = g.get_node_data(n_id)
    n_data.weight = n_weight
    n_data.backtrack_symbol = n_backtrack_symbol


# Walk back to get full sequence
backtrack_symbol = g.get_node_data('SINK').backtrack_symbol
emitted_symbols = [backtrack_symbol]
for i in range(n - 1, -1, -1):
    prev_backtrack_symbols = set()
    for hidden_state in hidden_states:
        n_id = i, hidden_state, backtrack_symbol
        n_data = g.get_node_data(n_id)
        prev_backtrack_symbols.add(n_data.backtrack_symbol)
    # assert len(prev_backtrack_symbols) == 1
    backtrack_symbol = next(iter(prev_backtrack_symbols))
    emitted_symbols.append(backtrack_symbol)
emitted_symbols.reverse()
emitted_symbols = emitted_symbols[1:]  # trim off source node's "backtracking symbol" because it's garbage


print(f'{g.get_node_data("SINK").weight}')  # OUTPUT SINK'S WEIGHT
print(emitted_symbols)


def to_dot(g: DirectedGraph.Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=TB]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = g.get_nodes()
    for n in nodes:
        ret += f'"{n}" [label="{n}\\n{g.get_node_data(n):.15f}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'"{n1}" -> "{n2}" [label="{weight:.3f}"]\n'
    ret += '}'
    return ret


print(f'{to_dot(g)}')

