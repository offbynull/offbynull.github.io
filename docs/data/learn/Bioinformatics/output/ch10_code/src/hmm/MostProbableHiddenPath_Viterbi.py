import math
from sys import stdin
from typing import TypeVar, Callable, Any

import yaml

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
STATE = TypeVar('STATE')
SYMBOL = TypeVar('SYMBOL')


def viterbi_to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        ret += f'"{n}" [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'"{n1}" -> "{n2}" [label="{weight}"]\n'
    ret += '}'
    return ret


# MARKDOWN_GENERATE_VITERBI
def to_viterbi_graph(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        hmm_sink_n_id: N,
        emissions: list[SYMBOL],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> Graph[tuple[int, N], Any, tuple[N, N], float]:
    viterbi = Graph()
    # Add Viterbi source node.
    viterbi_source_n_id = -1, hmm_source_n_id
    viterbi.insert_node(viterbi_source_n_id)
    # Explode out HMM into Viterbi.
    prev_nodes = {(hmm_source_n_id, viterbi_source_n_id)}
    emissions_idx = 0
    while prev_nodes and emissions_idx < len(emissions):
        symbol = emissions[emissions_idx]
        new_prev_nodes = set()
        for hmm_from_n_id, viterbi_from_n_id in prev_nodes:
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                viterbi_to_n_id = emissions_idx, hmm_to_n_id
                if not viterbi.has_node(viterbi_to_n_id):
                    viterbi.insert_node(viterbi_to_n_id)
                    new_prev_nodes.add((hmm_to_n_id, viterbi_to_n_id))
                hidden_state_transition_prob = get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
                symbol_emission_prob = get_node_emission_prob(hmm, hmm_to_n_id, symbol)
                viterbi_e_id = viterbi_from_n_id, viterbi_to_n_id
                viterbi_e_weight = hidden_state_transition_prob * symbol_emission_prob
                viterbi.insert_edge(
                    viterbi_e_id,
                    viterbi_from_n_id,
                    viterbi_to_n_id,
                    viterbi_e_weight
                )
        prev_nodes = new_prev_nodes
        emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to Viterbi.
    assert emissions_idx == len(emissions)
    # Add Viterbi sink node. Note that the HMM sink node ID doesn't have to exist in the HMM graph. It's only used to
    # represent a node in the Viterbi graph.
    viterbi_to_n_id = -1, hmm_sink_n_id
    viterbi.insert_node(viterbi_to_n_id)
    for hmm_from_n_id, viterbi_from_n_id in prev_nodes:
        viterbi_e_id = viterbi_from_n_id, viterbi_to_n_id
        viterbi_e_weight = 1.0
        viterbi.insert_edge(
            viterbi_e_id,
            viterbi_from_n_id,
            viterbi_to_n_id,
            viterbi_e_weight
        )
    return viterbi
# MARKDOWN_GENERATE_VITERBI


def hmm_to_dot(g: Graph) -> str:
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
        if len(transition_probabilities[from_state]) > 0:
            assert sum(prob for prob in transition_probabilities[from_state].values()) == 1.0
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
        if len(emission_probabilities[state]) > 0:
            assert sum(prob for prob in emission_probabilities[state].values()) == 1.0
        weights = emission_probabilities[state]
        if not hmm.has_node(state):
            hmm.insert_node(state)
        hmm.update_node_data(state, weights)
    return hmm


def main_generate_viterbi_structure():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        sink_state = data['sink_state']
        emissions = data['emissions']
        print(f'Building Viterbi graph using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        viterbi = to_viterbi_graph(
            hmm,
            source_state,
            sink_state,
            emissions,
            lambda g, state, symbol: g.get_node_data(state)[symbol],
            lambda g, s1, s2: g.get_edge_data((s1, s2))
        )
        print(f'The following Viterbi graph was produced for the HMM and the emitted sequence {emissions} ...')
        print()
        print('```{dot}')
        print(f'{viterbi_to_dot(viterbi)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")
















# MARKDOWN_MAX_PRODUCT_PATH_IN_VITERBI
def max_product_path_in_viterbi(
        viterbi: Graph[tuple[int, N], Any, tuple[N, N], float]
):
    # Backtrack to find path with max sum -- using logged weights, path with max sum is actually path with max product.
    # Note that the call to populate_weights_and_backtrack_pointers() below is taking the math.log() of the edge weight
    # rather than passing back the edge weight itself.
    source_n_id = viterbi.get_root_node()
    sink_n_id = viterbi.get_leaf_node()
    FindMaxPath_DPBacktrack.populate_weights_and_backtrack_pointers(
        viterbi,
        source_n_id,
        lambda n, w, e: viterbi.update_node_data(n, (w, e)),
        lambda n: viterbi.get_node_data(n),
        lambda e: -math.inf if viterbi.get_edge_data(e) == 0 else math.log(viterbi.get_edge_data(e)),
    )
    edges = FindMaxPath_DPBacktrack.backtrack(
        viterbi,
        sink_n_id,
        lambda n_id: viterbi.get_node_data(n_id)
    )
    path = []
    final_weight = 1.0
    for e_id in edges:
        _, from_node = viterbi.get_edge_from(e_id)
        _, to_node = viterbi.get_edge_to(e_id)
        path.append((from_node, to_node))
        weight = viterbi.get_edge_data(e_id)
        final_weight *= weight
    return final_weight, path
# MARKDOWN_MAX_PRODUCT_PATH_IN_VITERBI


def main_most_probable_hidden_path():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        sink_state = data['sink_state']
        emissions = data['emissions']
        print(f'Building Viterbi graph and finding the max product weight using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        viterbi = to_viterbi_graph(
            hmm,
            source_state,
            sink_state,
            emissions,
            lambda g, state, symbol: g.get_node_data(state)[symbol],
            lambda g, s1, s2: g.get_edge_data((s1, s2))
        )
        print(f'The following Viterbi graph was produced for the HMM and the emitted sequence {emissions} ...')
        print()
        print('```{dot}')
        print(f'{viterbi_to_dot(viterbi)}')
        print('```')
        print()
        weight, hidden_path = max_product_path_in_viterbi(viterbi)
        print(f'The hidden path with the max product weight in this Viterbi graph is {hidden_path} (max product weight = {weight}).')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")



























if __name__ == '__main__':
    main_most_probable_hidden_path()
