import lzma
import math
from collections import Counter
from itertools import product
from math import log
from typing import TypeVar

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph
from helpers.Utils import slide_window


# Exercise Break: Apply Viterbi learning to learn parameters for an HMM modeling CG-islands as well as for the profile
# HMM for the gp120 HIV alignment.

# MY ANSWER
# ---------
# This is the just code challenge. The GC problem is easy but th gp120 problem is more confusing: I'm having trouble
# understanding what this is asking for. For the gp120 profile, you already have parameters (state-state transition
# probabilities and state-symbol emission probabilities) since you already have a profile. Correct? Is it instead asking
# you to run each individual gp120 sequence through Viterbi learning, then somehow blend the weights?

def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = g.get_nodes()
    for n in nodes:
        data = g.get_node_data(n)
        ret += f'"{n}" [label="{n}\\n{data}"]\n'  # \\n{g.get_node_data(n)}
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        ret += f'"{n1}" -> "{n2}" [label="{data}"]\n'  # [label="{weight}"]
    ret += '}'
    return ret


def symbol_emitted_and_hidden_path_to_hmm_weights(
        states: list[str],
        symbols: list[str],
        hidden_path: list[str],
        emitted_seq: list[str]
) -> tuple[
     dict[tuple[str, str], float],
     dict[tuple[str, str], float]
]:
    state_transition_counts = Counter()
    total_state_transition_counts = Counter()
    for (from_s, to_s), _ in slide_window(hidden_path, 2):
        state_transition_counts[from_s, to_s] += 1
        total_state_transition_counts[from_s] += 1

    state_transition_weights = {}
    for from_s in states:
        for to_s in states:
            full_total = total_state_transition_counts[from_s]
            match_total = state_transition_counts[from_s, to_s]
            if full_total == 0:
                transition_weight = 1.0 / len(states)
            else:
                transition_weight = match_total / full_total
            state_transition_weights[from_s, to_s] = transition_weight

    state_emission_counts = Counter()
    total_state_emission_counts = Counter()
    for (state, symbol) in zip(hidden_path, emitted_seq):
        state_emission_counts[state, symbol] += 1
        total_state_emission_counts[state] += 1

    state_emission_weights = {}
    for state in states:
        for i, symbol in enumerate(symbols):
            full_total = total_state_emission_counts[state]
            match_total = state_emission_counts[state, symbol]
            if full_total == 0:
                emission_weight = 1.0 / len(symbols)
            else:
                emission_weight = match_total / full_total
            state_emission_weights[state, symbol] = emission_weight

    return state_transition_weights, state_emission_weights


def symbol_emitted_and_hmm_weights_to_hidden_path(
        states: list[str],
        emitted_seq: list[str],
        state_transition_weights: dict[tuple[str, str], float],
        state_emission_weights: dict[tuple[str, str], float]
):
    g = Graph()
    g.insert_node('SOURCE')
    for i in range(len(emitted_seq)):
        for state in states:
            g.insert_node(f'{state}{i}')
    g.insert_node('SINK')

    for to_state in states:
        g.insert_edge(
            f'SOURCE->{to_state}0',
            'SOURCE',
            f'{to_state}0',
            1.0
        )
    for (from_states, to_states), i in slide_window([list(states)] * len(emitted_seq), 2):
        symbol = emitted_seq[i]
        for from_state, to_state in product(from_states, to_states):
            weight = state_transition_weights[from_state, to_state] * state_emission_weights[from_state, symbol]
            g.insert_edge(
                f'{from_state}{i}->{to_state}{i + 1}',
                f'{from_state}{i}',
                f'{to_state}{i + 1}',
                weight
            )
    i = len(emitted_seq) - 1
    for to_state in states:
        g.insert_edge(
            f'{to_state}{i}->SINK',
            f'{to_state}{i}',
            'SINK',
            1.0
        )

    for e in list(g.get_edges()):
        weight = g.get_edge_data(e)
        log_weight = log(weight) if weight > 0 else -math.inf  # IMPORTANT -- SET TO -inf IF NOT USING PSEUDOCOUNTS
        g.update_edge_data(e, log_weight)

    # print(f'{to_dot(g)}')
    FindMaxPath_DPBacktrack.populate_weights_and_backtrack_pointers(
        g,
        'SOURCE',
        lambda n, w, e: g.update_node_data(n, (w, e)),
        lambda n: g.get_node_data(n),
        lambda e: g.get_edge_data(e),
    )
    final_weight, _ = g.get_node_data('SINK')
    edges = FindMaxPath_DPBacktrack.backtrack(
        g,
        'SINK',
        lambda n_id: g.get_node_data(n_id)
    )
    alignment = []
    for e in edges:
        to_node = g.get_edge_to(e)
        alignment.append(to_node[0:1])
    alignment = alignment[:-1]  # snip off sink node
    return alignment


with lzma.open('chrX_first_million.txt.xz', 'r') as f:
    seq = f.read().decode().upper()
seq_is_cg = []
for kmer, _ in slide_window(seq, 2):
    seq_is_cg.append('T' if kmer == 'CG' else 'F')

max_iterations = 10
emitted_seq = seq_is_cg
symbols = ['T', 'F']
states = ['Y', 'N']
state_transition_probs = {
    ('Y', 'N'): 0.001,
    ('Y', 'Y'): 0.999,
    ('N', 'Y'): 0.0001,
    ('N', 'N'): 0.9999,
}
state_emission_probs = {
    ('Y', 'T'): 0.3,
    ('Y', 'F'): 0.7,
    ('N', 'T'): 0.01,
    ('N', 'F'): 0.99,
}


for i in range(max_iterations):
    print(f'{i}')
    hidden_path = symbol_emitted_and_hmm_weights_to_hidden_path(states, emitted_seq, state_transition_probs, state_emission_probs)
    # print(f'{hidden_path=}')
    state_transition_probs, state_emission_probs = symbol_emitted_and_hidden_path_to_hmm_weights(states, symbols, hidden_path, emitted_seq)
    # print(f'{state_transition_probs=}')
    # print(f'{state_emission_probs=}')

print(f'\t', end='')
for from_state in states:
    print(f'{from_state}\t', end='')
print()
for from_state in states:
    print(f'{from_state}\t', end='')
    for to_state in states:
        print(f'{state_transition_probs[from_state, to_state]}\t', end='')
    print()

print('--------')

print(f'\t', end='')
for from_state in states:
    print(f'{from_state}\t', end='')
print()
for from_state in states:
    for i, symbol in enumerate(symbols):
        if i == 0:
            print(f'{symbol}\t', end='')
        print(f'{state_emission_probs[from_state, symbol]}\t', end='')
    print()
