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
def state_transition_chain_probability(
        hmm: Graph[N, ND, E, ED],
        states: list[STATE],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> float:
    weight = 1.0
    for (from_state, to_state), _ in slide_window(states, 2):
        weight *= get_edge_transition_prob(hmm, from_state, to_state)
    return weight
# MARKDOWN


def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        ret += f'"STATE_{n}" [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'"STATE_{n1}" -> "STATE_{n2}" [label="{weight}"]\n'
    added_symbols = set()
    for n in sorted(g.get_nodes()):
        emission_probs = g.get_node_data(n)
        for n_symbol, weight in emission_probs.items():
            if n_symbol not in added_symbols:
                ret += f'"SYMBOL_{n_symbol}" [label="{n_symbol}", style="dashed"]\n'
                added_symbols.add(n_symbol)
            ret += f'"STATE_{n}" -> "SYMBOL_{n_symbol}" [label="{weight}", style="dashed"]\n'
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







# transition_probabilities:
#   SOURCE: {A: 0.5, B: 0.5}
#   A: {A: 0.377, B: 0.623}
#   B: {A: 0.26, B: 0.74}
# emission_probabilities: # UNUSED
#   A: {}
#   B: {}
# states: [SOURCE, A, B, A, B, B ,B, A, A, A, A]

def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        states = data['states']
        print(f'Building HMM and computing transition / emission probability using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph(transition_probabilities, emission_probabilities)
        p = state_transition_chain_probability(
            hmm,
            states,
            lambda g, s1, s2: g.get_edge_data((s1, s2))
        )
        print()
        print(f'The following HMM was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(hmm)}')
        print('```')
        print()
        print(f'Probability of the chain of state transitions {list((a,b) for (a,b), _ in slide_window(states, 2))}'
              f' is {p}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()