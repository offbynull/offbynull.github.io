from sys import stdin
from typing import Generator

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot


# MARKDOWN
def enumerate_paths_targeting_transition_after_index(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_from_n_id: STATE,
        emitted_seq_len: int,
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE,
        prev_path: list[TRANSITION] | None = None,
        emission_idx: int = 0
) -> Generator[list[TRANSITION], None, None]:
    if prev_path is None:
        prev_path = []
    if emission_idx == emitted_seq_len:
        # We're at the end of the expected emitted sequence length, so return the current path. However, at this point
        # hmm_from_n_id may still have transitions to other non-emittable hidden states, and so those need to be
        # returned as paths as well (continue digging into outgoing transitions if the destination is non-emittable).
        yield prev_path
        for transition, hmm_from_n_id, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                continue
            if emission_idx == from_emission_idx + 1 and (hmm_from_n_id != from_hidden_state or hmm_to_n_id != to_hidden_state):
                continue
            prev_path.append(transition)
            yield from enumerate_paths_targeting_transition_after_index(hmm, hmm_to_n_id, emitted_seq_len,
                                                                        from_emission_idx, from_hidden_state,
                                                                        to_hidden_state, prev_path, emission_idx)
            prev_path.pop()
    else:
        # Explode out at that path by digging into transitions from hmm_from_n_id. When at from_emission_idx, only take
        # the transition from_hidden_state->to_hidden_state.
        for transition, hmm_from_n_id, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            if emission_idx == from_emission_idx + 1 and (hmm_from_n_id != from_hidden_state or hmm_to_n_id != to_hidden_state):
                continue
            prev_path.append(transition)
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                next_emission_idx = emission_idx + 1
            else:
                next_emission_idx = emission_idx
            yield from enumerate_paths_targeting_transition_after_index(hmm, hmm_to_n_id, emitted_seq_len,
                                                                        from_emission_idx, from_hidden_state,
                                                                        to_hidden_state, prev_path, next_emission_idx)
            prev_path.pop()


def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE,
) -> float:
    path_iterator = enumerate_paths_targeting_transition_after_index(
        hmm,
        hmm_source_n_id,
        len(emitted_seq),
        from_emission_idx,
        from_hidden_state,
        to_hidden_state
    )
    isolated_probs_sum = 0.0
    for path in path_iterator:
        isolated_probs_sum += probability_of_transitions_and_emissions(hmm, path, emitted_seq)
    return isolated_probs_sum


def probability_of_transitions_and_emissions(hmm, path, emitted_seq):
    emitted_seq_idx = 0
    prob = 1.0
    for transition in path:
        hmm_from_n_id, hmm_to_n_id = transition
        if hmm.get_node_data(hmm_to_n_id).is_emittable():
            symbol = emitted_seq[emitted_seq_idx]
            prob *= hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol) * \
                    hmm.get_edge_data(transition).get_transition_probability()
            emitted_seq_idx += 1
        else:
            prob *= hmm.get_edge_data(transition).get_transition_probability()
    return prob
# MARKDOWN


# transition_probs = {
#     'SOURCE': {'A': 0.5, 'B': 0.5},
#     'A': {'A': 0.377, 'B': 0.623},
#     'B': {'A': 0.301, 'C': 0.699},
#     'C': {'B': 1.0}
# }
# emission_probs = {
#     'SOURCE': {},
#     'A': {'x': 0.533, 'y': 0.065, 'z': 0.402},
#     'B': {'x': 0.342, 'y': 0.334, 'z': 0.324},
#     'C': {}
# }
# prob = emission_probability(
#     to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs),
#     'SOURCE',
#     list('yyzz'),
#     1,
#     'B',
#     'A'
# )
# print(f'{prob}')
# g = enumerate_paths_targeting_transition_after_index(
#     to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs),
#     'SOURCE',
#     4,
#     1,
#     'B',
#     'A'
# )
# for p in g:
#     print(f'{" * ".join(f"Pr({e[0]}→{e[1]})" for e in p)}')
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
        from_emission_idx = data['from_emission_idx']
        from_hidden_state = data['from_hidden_state']
        to_hidden_state = data['to_hidden_state']
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
            pseudocount
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount
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
            from_emission_idx,
            from_hidden_state,
            to_hidden_state
        )
        print(f'The probability of {emissions} being emitted when index {from_emission_idx} only has the option'
              f' to travel from {from_hidden_state} to {to_hidden_state} is {probability}.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
