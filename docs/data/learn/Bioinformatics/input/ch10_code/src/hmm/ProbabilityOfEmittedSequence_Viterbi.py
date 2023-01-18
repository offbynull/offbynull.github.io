import math
from sys import stdin
from typing import TypeVar, Callable, Any, Iterable

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


def to_viterbi_graph(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        hmm_sink_n_id: N,
        emissions: list[SYMBOL],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> Graph[tuple[int, N], Any, tuple[N, N], float]:
    viterbi = Graph()
    # Add Viterbi source node.
    viterbi_source_n_id = -1, hmm_source_n_id
    viterbi.insert_node(viterbi_source_n_id)
    # Explode out HMM into Viterbi.
    viterbi_from_n_emissions_idx = -1
    viterbi_from_n_ids = {viterbi_source_n_id}
    viterbi_to_n_emissions_idx = 0
    viterbi_to_n_ids_emitting = set()
    viterbi_to_n_ids_non_emitting = set()
    while viterbi_from_n_ids and viterbi_to_n_emissions_idx < len(emissions):
        viterbi_to_n_symbol = emissions[viterbi_to_n_emissions_idx]
        viterbi_to_n_ids_emitting = set()
        viterbi_to_n_ids_non_emitting = set()
        while viterbi_from_n_ids:
            viterbi_from_n_id = viterbi_from_n_ids.pop()
            _, hmm_from_n_id = viterbi_from_n_id
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emittable = get_node_emittable(hmm, hmm_to_n_id)
                if hmm_to_n_emittable:
                    hidden_state_transition_prob = get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
                    symbol_emission_prob = get_node_emission_prob(hmm, hmm_to_n_id, viterbi_to_n_symbol)
                    viterbi_to_n_id = viterbi_to_n_emissions_idx, hmm_to_n_id
                    connect_viterbi_nodes(
                        viterbi,
                        viterbi_from_n_id,
                        viterbi_to_n_id,
                        hidden_state_transition_prob * symbol_emission_prob
                    )
                    viterbi_to_n_ids_emitting.add(viterbi_to_n_id)
                else:
                    hidden_state_transition_prob = get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
                    viterbi_to_n_id = viterbi_from_n_emissions_idx, hmm_to_n_id
                    to_n_existed = connect_viterbi_nodes(
                        viterbi,
                        viterbi_from_n_id,
                        viterbi_to_n_id,
                        hidden_state_transition_prob
                    )
                    if not to_n_existed:
                        viterbi_from_n_ids.add(viterbi_to_n_id)
                    viterbi_to_n_ids_non_emitting.add(viterbi_to_n_id)
        viterbi_from_n_ids = viterbi_to_n_ids_emitting
        viterbi_from_n_emissions_idx += 1
        viterbi_to_n_emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to Viterbi.
    assert viterbi_to_n_emissions_idx == len(emissions)
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    viterbi_to_n_ids_non_emitting = set()
    viterbi_from_n_ids = viterbi_to_n_ids_emitting.copy()
    while viterbi_from_n_ids:
        viterbi_from_n_id = viterbi_from_n_ids.pop()
        _, hmm_from_n_id = viterbi_from_n_id
        for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            hmm_to_n_emmitable = get_node_emittable(hmm, hmm_to_n_id)
            if hmm_to_n_emmitable:
                continue
            hidden_state_transition_prob = get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
            viterbi_to_n_id = viterbi_from_n_emissions_idx, hmm_to_n_id
            connect_viterbi_nodes(
                viterbi,
                viterbi_from_n_id,
                viterbi_to_n_id,
                hidden_state_transition_prob
            )
            viterbi_to_n_ids_non_emitting.add(viterbi_to_n_id)
            viterbi_from_n_ids.add(viterbi_to_n_id)
    # Add Viterbi sink node.
    viterbi_to_n_id = -1, hmm_sink_n_id
    for viterbi_from_n_id in viterbi_to_n_ids_emitting | viterbi_to_n_ids_non_emitting:
        connect_viterbi_nodes(viterbi, viterbi_from_n_id, viterbi_to_n_id, 1.0)
    return viterbi


def connect_viterbi_nodes(
        viterbi: Graph[tuple[int, N], Any, tuple[N, N], float],
        viterbi_from_n_id: tuple[int, N],
        viterbi_to_n_id: tuple[int, N],
        weight: float
) -> bool:
    to_n_existed = True
    if not viterbi.has_node(viterbi_to_n_id):
        viterbi.insert_node(viterbi_to_n_id)
        to_n_existed = False
    viterbi_e_weight = weight
    viterbi_e_id = viterbi_from_n_id, viterbi_to_n_id
    viterbi.insert_edge(
        viterbi_e_id,
        viterbi_from_n_id,
        viterbi_to_n_id,
        viterbi_e_weight
    )
    return to_n_existed


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


def to_hmm_graph_PRE_PSEUDOCOUNTS(
        transition_probabilities: dict[str, dict[str, float]],
        emission_probabilities: dict[str, dict[str, float]]
) -> Graph[str, dict[str, float], tuple[str, str], float]:
    # Does not check that all outgoing transitions sum to 1.0 / all emissions sum to 1.0. These checks need to be done
    # after pseudocounts are applied
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


def hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm: Graph[N, ND, E, ED],
        psuedocount: float,
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_outgoing_state_transitions: [[Graph[N, ND, E, ED], STATE], Iterable[STATE]],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float],
        set_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE, float], None]
) -> None:
    for from_state in list_states(hmm):
        tweaked_transition_weights = {}
        total_transition_weights = 0.0
        for to_state in list_outgoing_state_transitions(hmm, from_state):
            weight = get_edge_transition_prob(hmm, from_state, to_state) + psuedocount
            tweaked_transition_weights[to_state] = weight
            total_transition_weights += weight
        for to_state, weight in tweaked_transition_weights.items():
            normalized_transition_weight = weight / total_transition_weights
            set_edge_transition_prob(hmm, from_state, to_state, normalized_transition_weight)


def hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm: Graph[N, ND, E, ED],
        psuedocount: float,
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_state_emissions: [[Graph[N, ND, E, ED]], Iterable[SYMBOL]],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        set_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL, float], None],
) -> None:
    for from_state in list_states(hmm):
        tweaked_emission_weights = {}
        total_emission_weights = 0.0
        for symbol in list_state_emissions(hmm, from_state):
            weight = get_node_emission_prob(hmm, from_state, symbol) + psuedocount
            tweaked_emission_weights[symbol] = weight
            total_emission_weights += weight
        for symbol, weight in tweaked_emission_weights.items():
            normalized_transition_weight = weight / total_emission_weights
            set_node_emission_prob(hmm, from_state, symbol, normalized_transition_weight)


# MARKDOWN
def emission_probability(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        hmm_sink_n_id: N,
        emitted_seq: list[SYMBOL],
        hidden_states: set[STATE],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
):
    viterbi = to_viterbi_graph(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq, get_node_emission_prob,
                               get_node_emittable, get_edge_transition_prob)
    viterbi_source_n_id = viterbi.get_root_node()  # equiv to (-1, hmm_source_n_id) -- using root node func for clarity
    viterbi.update_node_data(viterbi_source_n_id, 1.0)
    for i, symbol in enumerate(emitted_seq):
        for state in hidden_states:
            to_n_id = i, state
            n_forward_weight = 0.0
            for e_id, from_n, _, e_weight in viterbi.get_inputs_full(to_n_id):
                from_n_forward_weight = get_edge_transition_prob(hmm, from_n[1], to_n_id[1])
                n_forward_weight += from_n_forward_weight * from_n_forward_weight
            if get_node_emittable(hmm, state):
                symbol_emission_prob = get_node_emission_prob(hmm, state, symbol)
            else:
                symbol_emission_prob = 1.0
            n_forward_weight *= symbol_emission_prob
            viterbi.update_node_data(to_n_id, n_forward_weight)

    # Now do it for the sink as well
    viterbi_sink_n_id = viterbi.get_leaf_node()  # equiv to (-1, hmm_sink_n_id) -- using leaf node func for clarity
    n_forward_weight = 0.0
    for e_id, from_n, _, e_weight in viterbi.get_inputs_full(viterbi_sink_n_id):
        from_n_forward_weight = viterbi.get_node_data(from_n)
        n_forward_weight += from_n_forward_weight * e_weight
    viterbi.update_node_data(viterbi_sink_n_id, n_forward_weight)

    return n_forward_weight
# MARKDOWN


transition_probs = {
    'SOURCE': {'A': 0.5, 'B': 0.5},
    'A': {'A': 0.303, 'B': 0.697},
    'B': {'A': 0.831, 'B': 0.169},
}
emission_probs = {
    'A': {'x': 0.533, 'y': 0.065, 'z': 0.402},
    'B': {'x': 0.342, 'y': 0.334, 'z': 0.324}
}
prob = emission_probability(
    to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs),
    'SOURCE',
    'SINK',
    list('xzyyzzyzyy'),
    {'A', 'B'},
    lambda g, st, sy: emission_probs[st][sy],
    lambda g, st: emission_probs[st] != {},
    lambda g, st1, st2: transition_probs[st1][st2]
)
print(f'{prob}')


def main():
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
        pseudocount = data['pseudocount']
        print(f'Building Viterbi graph (with non-emitting hidden states) and finding the max product weight, after applying psuedocounts to HMM, using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced before applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
            hmm,
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: [s2 for _, _, s2, _ in g.get_outputs_full(s1)],
            lambda g, s1, s2: g.get_edge_data((s1, s2)),
            lambda g, s1, s2, weight: g.update_edge_data((s1, s2), weight)
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: list(g.get_node_data(s1)),
            lambda g, s1, sym: g.get_node_data(s1)[sym],
            lambda g, s1, sym, weight: g.get_node_data(s1).update({sym: weight})
        )
        print(f'After pseudocounts are applied, the HMM becomes as follows ...')
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
            lambda g, state: g.get_node_data(state) != {},
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
    main()
