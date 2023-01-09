import math
from collections import Counter
from itertools import product
from math import log
from typing import TypeVar

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph
from helpers.Utils import slide_window




# Exercise Break: Consider the following questions.
#
# * For the crooked dealer HMM, compute Pr(πi = k|x) for x = “THTHHHTHTTH” and each value of i. How does your answer
#   change if x = “HHHHHHHHHHH”?
# * Apply your solution for the Soft Decoding Problem to find CG-islands in the first million nucleotides from the human
#   X chromosome. How does your answer differ from the solution given by the Viterbi algorithm?


# MY ANSWER
# ---------
# I'm only going to do this for the crooked dealer HMM. All H's is stating that the biased coin was used during each
# flip.


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


def forward(
        states: list[str],
        emitted_seq: list[str],
        state_transition_probs: dict[tuple[str, str], float],
        state_emission_probs: dict[tuple[str, str], float]
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
            f'SOURCE',
            f'{to_state}0',
            (1.0 / len(states), 'SOURCE', to_state)
        )
    for (from_states, to_states), i in slide_window([list(states)] * len(emitted_seq), 2):
        for from_state, to_state in product(from_states, to_states):
            g.insert_edge(
                f'{from_state}{i}->{to_state}{i + 1}',
                f'{from_state}{i}',
                f'{to_state}{i + 1}',
                (state_transition_probs[from_state, to_state], from_state, to_state)
            )
    i = len(emitted_seq) - 1
    for to_state in states:
        g.insert_edge(
            f'{to_state}{i}->SINK',
            f'{to_state}{i}',
            'SINK',
            (1.0, to_state, 'SINK')
        )

    g.update_node_data('SOURCE', 1.0)
    for i, symbol in enumerate(emitted_seq):
        for state in states:
            n_id = f'{state}{i}'
            n_forward_weight = 0.0
            for e_id, from_n, _, e_data in g.get_inputs_full(n_id):
                from_n_forward_weight = g.get_node_data(from_n)
                transition_weight = e_data[0]
                n_forward_weight += from_n_forward_weight * transition_weight
            n_forward_weight *= state_emission_probs[state, symbol]
            g.update_node_data(n_id, n_forward_weight)

    # Now do it for the sink as well
    n_forward_weight = 0.0
    for e_id, from_n, _, e_data in g.get_inputs_full('SINK'):
        from_n_forward_weight = g.get_node_data(from_n)
        transition_weight = e_data[0]
        n_forward_weight += from_n_forward_weight * transition_weight
    g.update_node_data('SINK', n_forward_weight)

    return g


def backward(
        states: list[str],
        emitted_seq: list[str],
        state_transition_probs: dict[tuple[str, str], float],
        state_emission_probs: dict[tuple[str, str], float]
):
    g = Graph()
    g.insert_node('SOURCE')
    for i in range(len(emitted_seq)):
        for from_state in states:
            g.insert_node(f'{from_state}{i}')
    g.insert_node('SINK')

    for to_state in states:
        g.insert_edge(
            f'SOURCE<-{to_state}0',
            f'{to_state}0',
            f'SOURCE',
            (1.0 / len(states), to_state, 'SOURCE')
        )
    for (from_states, to_states), i in slide_window([list(states)] * len(emitted_seq), 2):
        for from_state, to_state in product(from_states, to_states):
            g.insert_edge(
                f'{from_state}{i}<-{to_state}{i + 1}',
                f'{to_state}{i + 1}',
                f'{from_state}{i}',
                (state_transition_probs[from_state, to_state], from_state, to_state)
            )
    i = len(emitted_seq) - 1
    for to_state in states:
        g.insert_edge(
            f'{to_state}{i}<-SINK',
            'SINK',
            f'{to_state}{i}',
            (1.0, 'SINK', to_state)
        )

    g.update_node_data('SINK', 1.0)
    for i, symbol in reversed(list(enumerate(emitted_seq[1:] + [None]))):
        for from_state in states:
            n_id = f'{from_state}{i}'
            if i == len(emitted_seq) - 1:
                n_backward_weight = 1.0
            else:
                n_backward_weight = 0.0
                for e_id, from_n, _, e_data in g.get_inputs_full(n_id):
                    from_n_backward_weight = g.get_node_data(from_n)
                    transition_weight = e_data[0]
                    to_state = e_data[2]
                    n_backward_weight += from_n_backward_weight * transition_weight * state_emission_probs[to_state, symbol]
            g.update_node_data(n_id, n_backward_weight)

    # Now do it for the source as well
    n_backward_weight = 0.0
    for e_id, from_n, _, e_data in g.get_inputs_full('SOURCE'):
        from_n_backward_weight = g.get_node_data(from_n)
        transition_weight = e_data[0]
        n_backward_weight += from_n_backward_weight * transition_weight  # no symbol emitted? set a fake state_emission prob of 0?
    g.update_node_data('SOURCE', n_backward_weight)

    return g


def run(
        states: list[str],
        emitted_seq: list[str],
        state_transition_probs: dict[tuple[str, str], float],
        state_emission_probs: dict[tuple[str, str], float]
):
    forward_g = forward(states, emitted_seq, state_transition_probs, state_emission_probs)
    # print(f'{to_dot(forward_g)}')
    backward_g = backward(states, emitted_seq, state_transition_probs, state_emission_probs)
    # print(f'{to_dot(backward_g)}')
    for state in states:
        print(f'{state}\t', end='')
    print()
    for idx, symbol in enumerate(emitted_seq):
        for state in states:
            f = forward_g.get_node_data(f'{state}{idx}')
            b = backward_g.get_node_data(f'{state}{idx}')
            f_sink = forward_g.get_node_data(f'SINK')
            p = (f * b) / f_sink
            print(f'{p}\t', end='')
        print()


symbols = ['T', 'H']
states = ['F', 'B']
state_transition_probs = {
    ('F', 'F'): 0.1,
    ('F', 'B'): 0.1,
    ('B', 'F'): 0.1,
    ('B', 'B'): 0.1
}
state_emission_probs = {
    ('F', 'H'): 0.5,
    ('F', 'T'): 0.5,
    ('B', 'H'): 0.75,
    ('B', 'T'): 0.25
}


emitted_seq = list('THTHHHTHTTH')
print(f'{emitted_seq}')
run(states, emitted_seq, state_transition_probs, state_emission_probs)

emitted_seq = list('HHHHHHHHHHH')
print(f'{emitted_seq}')
run(states, emitted_seq, state_transition_probs, state_emission_probs)
