from sys import stdin
from typing import TypeVar, Callable, Iterable

import yaml

from graph.DirectedGraph import Graph
from helpers.Utils import slide_window

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
STATE = TypeVar('STATE')
SYMBOL = TypeVar('SYMBOL')


# MARKDOWN
def state_transition_followed_by_symbol_emission_chain_probability(
        hmm: Graph[N, ND, E, ED],
        source_state: STATE,
        state_symbol_pairs: list[tuple[STATE, SYMBOL]],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> float:
    to_state, to_symbol = state_symbol_pairs[0]
    weight = get_edge_transition_prob(hmm, source_state, to_state) * get_node_emission_prob(hmm, to_state, to_symbol)
    for ((from_state, _), (to_state, to_symbol)), _ in slide_window(state_symbol_pairs, 2):
        weight *= get_edge_transition_prob(hmm, from_state, to_state) * get_node_emission_prob(hmm, to_state, to_symbol)
    return weight
# MARKDOWN


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


def to_hmm_graph(
        transition_probabilities: dict[str, dict[str, float]],
        emission_probabilities: dict[str, dict[str, float]]
) -> Graph[str, dict[str, float], tuple[str, str], float]:
    hmm = Graph()
    for from_state in transition_probabilities:
        if not hmm.has_node(from_state):
            hmm.insert_node(from_state)
        for to_state, weight in transition_probabilities[from_state].items():
            if not hmm.has_node(to_state):
                hmm.insert_node(to_state)
            hmm.insert_edge(
                (from_state, to_state),
                from_state,
                to_state,
                weight
            )
    for state in emission_probabilities:
        weights = emission_probabilities[state]
        if not hmm.has_node(state):
            hmm.insert_node(state)
        hmm.update_node_data(state, weights)
    return hmm


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        state_symbol_pairs = [tuple(e) for e in data['state_emissions']]
        print(f'Building HMM and computing transition / emission probability using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph(transition_probabilities, emission_probabilities)
        p = state_transition_followed_by_symbol_emission_chain_probability(
            hmm,
            source_state,
            state_symbol_pairs,
            lambda g, state, symbol: g.get_node_data(state)[symbol],
            lambda g, s1, s2: g.get_edge_data((s1, s2))
        )
        print()
        print(f'The following HMM was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(hmm)}')
        print('```')
        print()
        print(f'Probability of traveling through {[source_state] + [x[0] for x in state_symbol_pairs]}, where after each'
              f' state transition results in the emissions {[x[1] for x in state_symbol_pairs]}, is {p}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
