import math
from sys import stdin
from typing import TypeVar, Callable, Any, Iterable, Generator

import yaml

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
STATE = TypeVar('STATE')
SYMBOL = TypeVar('SYMBOL')


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
def enumerate_paths(
        hmm: Graph[N, ND, E, ED],
        hmm_from_n_id: N,
        emitted_seq_len: int,
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        prev_path: list[E] | None = None
) -> Generator[list[E], None, None]:
    if prev_path is None:
        prev_path = []
    if emitted_seq_len == 0:
        # We're at the end of the expected emitted sequence length, so return the current path. However, at this point
        # hmm_from_n_id may still have transitions to other non-emittable hidden states, and so those need to be
        # returned as paths as well (continue digging into outgoing transitions if the destination is non-emittable).
        yield prev_path
        for hmm_e_id, _, hmm_to_n_id, transition_prob in hmm.get_outputs_full(hmm_from_n_id):
            if get_node_emittable(hmm, hmm_to_n_id):
                continue
            prev_path.append(hmm_e_id)
            yield from enumerate_paths(hmm, hmm_to_n_id, emitted_seq_len, get_node_emittable, prev_path)
            prev_path.pop()
    else:
        # Explode out at that path by digging into transitions from hmm_from_n_id. If the destination of the transition
        # is an ...
        # * emittable hidden state, subtract the expected emitted sequence length by 1 when you dig down.
        # * non-emittable hidden state, keep the expected emitted sequence length the same when you dig down.
        for hmm_e_id, _, hmm_to_n_id, transition_prob in hmm.get_outputs_full(hmm_from_n_id):
            prev_path.append(hmm_e_id)
            if get_node_emittable(hmm, hmm_to_n_id):
                next_emittable_seq_len = emitted_seq_len - 1
            else:
                next_emittable_seq_len = emitted_seq_len
            yield from enumerate_paths(hmm, hmm_to_n_id, next_emittable_seq_len, get_node_emittable, prev_path)
            prev_path.pop()


def emission_probability(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        emitted_seq: list[SYMBOL],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
):
    sum_of_probs = 0.0
    for p in enumerate_paths(hmm, hmm_source_n_id, len(emitted_seq), get_node_emittable):
        emitted_seq_idx = 0
        prob = 1.0
        for e_id in p:
            hmm_from_n_id, hmm_to_n_id, transition_prob = hmm.get_edge(e_id)
            if get_node_emittable(hmm, hmm_to_n_id):
                symbol = emitted_seq[emitted_seq_idx]
                prob *= get_node_emission_prob(hmm, hmm_to_n_id, symbol) *\
                        get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
                emitted_seq_idx += 1
            else:
                prob *= get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
        sum_of_probs += prob
    return sum_of_probs
# MARKDOWN


# transition_probs = {
#     'SOURCE': {'A': 0.5, 'B': 0.5},
#     'A': {'A': 0.377, 'B': 0.623},
#     'B': {'A': 0.301, 'C': 0.699},
#     'C': {'B': 1.0}
# }
# emission_probs = {
#     'A': {'x': 0.533, 'y': 0.065, 'z': 0.402},
#     'B': {'x': 0.342, 'y': 0.334, 'z': 0.324},
#     'C': {}
# }
# prob = emission_probability(
#     to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs),
#     'SOURCE',
#     list('xzyyzzyzyy'),
#     lambda g, st, sy: emission_probs[st][sy],
#     lambda g, st: emission_probs[st] != {},
#     lambda g, st1, st2: transition_probs[st1][st2]
# )
# print(f'{prob}')
# g = enumerate_paths(
#     to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs),
#     'SOURCE',
#     3,
#     lambda g, state: g.get_node_data(state) != {}
# )
# for p in g:
#     print(f'{" * ".join(f"Pr({e[0]}→{e[1]}|)" for e in p)}')
# raise ValueError()


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        emissions = data['emissions']
        pseudocount = data['pseudocount']
        print(f'Finding the probability of an HMM emitting a sequence, using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
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
        print(f'The following HMM was produced AFTER applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        probability = emission_probability(
            hmm,
            source_state,
            emissions,
            lambda g, state, symbol: g.get_node_data(state)[symbol],
            lambda g, state: g.get_node_data(state) != {},
            lambda g, s1, s2: g.get_edge_data((s1, s2))
        )
        print(f'The probability of {emissions} being emitted is {probability} ...')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







if __name__ == '__main__':
    main()
