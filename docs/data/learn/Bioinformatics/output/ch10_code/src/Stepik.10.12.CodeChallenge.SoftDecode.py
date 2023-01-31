import math
from collections import Counter
from itertools import product
from math import log
from typing import TypeVar

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph
from helpers.Utils import slide_window


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



with open('/home/user/Downloads/test.txt') as f:
    lines = f.read().splitlines(keepends=False)
emitted_seq = list(lines[0])
symbols = lines[2].split()
states = lines[4].split()
mat_head = lines[6].split()
state_transition_probs = {}
for mat_row in lines[7:7+len(states)]:
    mat_row = mat_row.split()
    state = mat_row[0]
    for i, to_state in enumerate(mat_head):
        state_transition_probs[state, to_state] = float(mat_row[i + 1])
state_emission_probs = {}
mat_head = lines[7+len(states)+1].split()
for mat_row in lines[7+len(states)+2:]:
    mat_row = mat_row.split()
    state = mat_row[0]
    for i, symbol in enumerate(mat_head):
        state_emission_probs[state, symbol] = float(mat_row[i + 1])


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
