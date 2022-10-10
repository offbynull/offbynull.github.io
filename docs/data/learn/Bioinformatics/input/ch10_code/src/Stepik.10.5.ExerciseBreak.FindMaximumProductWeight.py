from itertools import product

from graph import DirectedGraph
from helpers.Utils import slide_window

# Exercise Break: Exercise Break: Find the maximum product weight path in the Viterbi graph for the crooked dealer HMM
# (whose HMM diagram is reproduced below) when x = “HHTT”.  Express your answer as a string of four "F" and "B" symbols.
#
# State transitions:
# F->F=0.9, B->B=0.9, F->B=0.1, B->F=0.1
#
# Emissions:
# F->H=0.5,  F->T=0.5
# B->H=0.75, B->T=0.25
#
# Pr(x, π) = Pr(x|π) · Pr(π)


# MY ANSWER
# ---------
# Construct Viterbi graph
# Pr(π) = 0.5 * multiply(for x in slide_window(FFFBBBBBFFF, 2)) = 0.002152336050000001
# Pr(x|π) = multiply(Pr(a,b) for a, b in zip(FFFBBBBBFFF, THTHHHTHTTH)) = 0.0012359619140625
# Pr(x, π) = Pr(x|π) · Pr(π)
def to_dot(g: DirectedGraph.Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=TB]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n} [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -> {n2} [label="{weight}"]\n'
    ret += '}'
    return ret


hidden_states = {'F', 'B'}
hidden_state_transition_probs = {('F', 'F'): 0.9, ('B', 'B'): 0.9, ('F', 'B'): 0.1, ('B', 'F'): 0.1}
symbols = {'T', 'H'}
state_symbol_emission_probs = {('F', 'H'): 0.5, ('F', 'T'): 0.5, ('B', 'H'): 0.75, ('B', 'T'): 0.25}

hidden_state_transition_to_emission_probs = {}
for from_state, to_state, symbol in product(hidden_states, hidden_states, symbols):
    prob = hidden_state_transition_probs[(from_state, to_state)] * state_symbol_emission_probs[(to_state, symbol)]
    hidden_state_transition_to_emission_probs[from_state, to_state, symbol] = prob

for from_state, to_state, symbol in product({'SOURCE'}, hidden_states, symbols):
    prob = 1.0 / len(symbols) * state_symbol_emission_probs[(to_state, symbol)]
    hidden_state_transition_to_emission_probs[from_state, to_state, symbol] = prob

emitted_symbols = list('HHTT')
g = DirectedGraph.Graph()
g.insert_node('SOURCE')
for i, _ in enumerate(emitted_symbols):
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
for (from_states, to_states), i in slide_window([list(hidden_states)] * len(emitted_symbols), 2):
    symbol = emitted_symbols[i]
    for from_state, to_state in product(from_states, to_states):
        g.insert_edge(
            f'{from_state}{i}->{to_state}{i + 1}',
            f'{from_state}{i}',
            f'{to_state}{i + 1}',
            hidden_state_transition_to_emission_probs[from_state, to_state, symbol]
        )
symbol = emitted_symbols[-1]
i = len(emitted_symbols) - 1
for from_state, to_state in product(hidden_states, hidden_states):
    g.insert_edge(
        f'{from_state}{i}->{to_state}{i + 1}',
        f'{from_state}{i}',
        f'SINK',
        hidden_state_transition_to_emission_probs[from_state, to_state, symbol]
    )

print(f'{to_dot(g)}')

# LOOKS LIKE THIS IS ALL BIAS COINS: THE CALC IS ...
print(f'{1.0*0.45*0.45*0.45*0.45=}')

THIS SITE ISNT ACCEPTING THIS ANSWER. FIX FIX FIX FIX
THIS SITE ISNT ACCEPTING THIS ANSWER. FIX FIX FIX FIX
THIS SITE ISNT ACCEPTING THIS ANSWER. FIX FIX FIX FIX
THIS SITE ISNT ACCEPTING THIS ANSWER. FIX FIX FIX FIX
THIS SITE ISNT ACCEPTING THIS ANSWER. FIX FIX FIX FIX
THIS SITE ISNT ACCEPTING THIS ANSWER. FIX FIX FIX FIX
