import lzma
from itertools import product
from math import log

from graph import DirectedGraph
from helpers.Utils import slide_window
import find_max_path.FindMaxPath_DPBacktrack

# Exercise Break: Apply your solution for the Decoding Problem to find CG-islands in the first million nucleotides from
# the human X chromosome (given in FASTA format). To help you design an HMM for this application, you may assume that
# transitions from CG-islands to non-CG-islands are rare, occurring with probability 0.001, and that transitions from
# non-CG-islands to CG-islands are even more rare, occurring with probability 0.0001. How many CG-islands do you find?


# MY ANSWER
# ---------
with lzma.open('chrX_first_million.txt.xz', 'r') as f:
    seq = f.read().decode().upper()
seq_is_cg = ''
for kmer, _ in slide_window(seq, 2):
    seq_is_cg += 'T' if kmer == 'CG' else 'F'

emitted_symbols = seq_is_cg
symbols = {'T', 'F'}
hidden_states = {'Y', 'N'}
hidden_state_transition_probs = {
    ('Y', 'N'): 0.001,
    ('Y', 'Y'): 0.999,
    ('N', 'Y'): 0.0001,
    ('N', 'N'): 0.9999,
}
state_symbol_emission_probs = {
    ('Y', 'T'): 0.99,
    ('Y', 'F'): 0.01,
    ('N', 'T'): 0.25,
    ('N', 'F'): 0.75,
}

hidden_state_transition_to_emission_probs = {}
for from_state, to_state, symbol in product(hidden_states, hidden_states, symbols):
    prob = hidden_state_transition_probs[(from_state, to_state)] * state_symbol_emission_probs[(to_state, symbol)]
    hidden_state_transition_to_emission_probs[from_state, to_state, symbol] = prob

for from_state, to_state, symbol in product({'SOURCE'}, hidden_states, symbols):
    prob = 1.0 / len(symbols) * state_symbol_emission_probs[(to_state, symbol)]
    hidden_state_transition_to_emission_probs[from_state, to_state, symbol] = prob

g = DirectedGraph.Graph()
g.insert_node('SOURCE')
for i in range(len(emitted_symbols) + 1):
    for state in hidden_states:
        g.insert_node(f'{state}{i}')
g.insert_node('SINK')

for to_state in hidden_states:
    g.insert_edge(
        f'SOURCE->{to_state}0',
        'SOURCE',
        f'{to_state}0',
        1.0
    )
for (from_states, to_states), i in slide_window([list(hidden_states)] * (len(emitted_symbols) + 1), 2):
    symbol = emitted_symbols[i]
    for from_state, to_state in product(from_states, to_states):
        g.insert_edge(
            f'{from_state}{i}->{to_state}{i + 1}',
            f'{from_state}{i}',
            f'{to_state}{i + 1}',
            hidden_state_transition_to_emission_probs[from_state, to_state, symbol]
        )
i = len(emitted_symbols) - 1
for to_state in hidden_states:
    g.insert_edge(
        f'{to_state}{i + 1}->SINK',
        f'{to_state}{i + 1}',
        'SINK',
        1.0
    )

for e in list(g.get_edges()):
    weight = g.get_edge_data(e)
    log_weight = log(weight)
    g.update_edge_data(e, log_weight)

find_max_path.FindMaxPath_DPBacktrack.populate_weights_and_backtrack_pointers(
    g,
    'SOURCE',
    lambda n, w, e: g.update_node_data(n, (w, e)),
    lambda n: g.get_node_data(n),
    lambda e: g.get_edge_data(e),
)
final_weight, _ = g.get_node_data('SINK')
edges = find_max_path.FindMaxPath_DPBacktrack.backtrack(
    g,
    'SINK',
    lambda n_id: g.get_node_data(n_id)
)
alignment = []
for e in edges:
    to_node = g.get_edge_to(e)
    alignment.append(to_node[:1])
alignment = alignment[1:-1]  # snip off sink node
print(f'{"".join(alignment)}')

def to_dot(g: DirectedGraph.Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=TB]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n} [label="{n}\\n{g.get_node_data(n)[0]:.3f}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -> {n2} [label="{weight:.3f}"]\n'
    ret += '}'
    return ret


# print(f'{to_dot(g)}')