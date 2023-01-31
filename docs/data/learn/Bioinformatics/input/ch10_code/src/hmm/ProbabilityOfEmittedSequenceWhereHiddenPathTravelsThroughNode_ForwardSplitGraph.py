from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import forward_explode_hmm, forward_exploded_hmm_calculation, \
    exploded_to_dot, FORWARD_EXPLODED_NODE_ID


# MARKDOWN
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    f_exploded_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    # Isolate left-hand side and compute
    f_exploded_lhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    remove_after_node(f_exploded_lhs, f_exploded_n_id, hmm_sink_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Isolate right-hand side and compute
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    remove_before_node(f_exploded_rhs, f_exploded_n_id, hmm, hmm_source_n_id, hmm_sink_n_id)
    f_exploded_rhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_rhs, emitted_seq)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * f_exploded_rhs_sink_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (f_exploded_rhs, f_exploded_rhs_sink_weight),\
           f_exploded_sink_weight


def remove_after_node(
        f_exploded: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_n_id: FORWARD_EXPLODED_NODE_ID,
        hmm_sink_n_id: STATE
):
    emitted_seq_idx_of_interest, hidden_state_of_interest = f_exploded_n_id
    for f_exploded_test_n_id in set(f_exploded.get_nodes()):
        emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
        if (emitted_seq_idx == emitted_seq_idx_of_interest and hmm_n_id != hidden_state_of_interest)\
                or emitted_seq_idx > emitted_seq_idx_of_interest\
                or hmm_n_id == hmm_sink_n_id:
            delete_exploded_n_id = emitted_seq_idx, hmm_n_id
            f_exploded.delete_node(delete_exploded_n_id)
    # By deleting emitting hidden states in emitted_seq_idx_of_interest but not deleting non-emitting hidden states,
    # those non-emitting hidden states may have been orphaned (they've been disconnected from the main graph). Attempt
    # to clean them up here.
    filtered = True
    while filtered:
        filtered = False
        for f_exploded_test_n_id in set(f_exploded.get_root_nodes()):
            emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
            if emitted_seq_idx == emitted_seq_idx_of_interest and f_exploded_n_id != f_exploded_test_n_id:
                f_exploded.delete_node(f_exploded_test_n_id)
                filtered = True


def remove_before_node(
        f_exploded: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_n_id: FORWARD_EXPLODED_NODE_ID,
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE
):
    emitted_seq_idx_of_interest, hidden_state_of_interest = f_exploded_n_id
    for f_exploded_test_n_id in set(f_exploded.get_nodes()):
        emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
        if (emitted_seq_idx < emitted_seq_idx_of_interest and hmm_n_id != hmm_sink_n_id)\
                or (emitted_seq_idx == emitted_seq_idx_of_interest and hmm_n_id != hidden_state_of_interest and
                    hmm.get_node_data(hmm_n_id).is_emittable())\
                or hmm_n_id == hmm_source_n_id:
            delete_exploded_n_id = emitted_seq_idx, hmm_n_id
            f_exploded.delete_node(delete_exploded_n_id)
    # By deleting emitting hidden states in emitted_seq_idx_of_interest but not deleting non-emitting hidden states,
    # those non-emitting hidden states may have been orphaned (they've been disconnected from the main graph). Attempt
    # to clean them up here.
    filtered = True
    while filtered:
        filtered = False
        for f_exploded_test_n_id in set(f_exploded.get_root_nodes()):
            emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
            if emitted_seq_idx == emitted_seq_idx_of_interest and f_exploded_n_id != f_exploded_test_n_id:
                f_exploded.delete_node(f_exploded_test_n_id)
                filtered = True
# MARKDOWN


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
        emission_idx_of_interest = data['emission_index_of_interest']
        hidden_state_of_interest = data['hidden_state_of_interest']
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
        (f_exploded_lhs, f_exploded_lhs_prob_sum), \
        (f_exploded_rhs, f_exploded_rhs_prob_sum), \
        probability = emission_probability(
            hmm,
            source_state,
            sink_state,
            emissions,
            emission_idx_of_interest,
            hidden_state_of_interest
        )
        print()
        print(f'The exploded HMM was modified such that index {emission_idx_of_interest} only has the option to'
              f' {hidden_state_of_interest}, then split based on that node.')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded_lhs, label="Left-hand side", label_loc="top")}')
        print('```')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded_rhs, label="Right-hand side", label_loc="top")}')
        print('```')
        print()
        print(f' * The left-hand side is computed to have {f_exploded_lhs_prob_sum} at its sink node.')
        print(f' * The right-hand side is is computed to have {f_exploded_rhs_prob_sum} at its sink node.')
        print()
        print(f'When the sink nodes are multiplied together, its the probability for all hidden paths that travel'
              f' through {hidden_state_of_interest} at index {emission_idx_of_interest} of {emissions}. The probability'
              f' of {emissions} being emitted when index {emission_idx_of_interest} only has the option to emit from'
              f' {hidden_state_of_interest} is {probability}.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


# def test():
#     transition_probabilities = {
#       'SOURCE': {'A': 0.5, 'B': 0.5},
#       'A': {'A': 0.377, 'B': 0.623},
#       'B': {'A': 0.301, 'C': 0.699},
#       'C': {'B': 1.0}
#     }
#     emission_probabilities = {
#       'SOURCE': {},
#       'A': {'x': 0.176, 'y': 0.596, 'z': 0.228},
#       'B': {'x': 0.225, 'y': 0.572, 'z': 0.203},
#       'C': {}
#       # C set to empty dicts to identify as non-emittable hidden state.
#     }
#     source_state = 'SOURCE'
#     sink_state = 'SINK'
#     emissions = list('zzy')
#     emission_index_of_interest = 2
#     hidden_state_of_interest = 'B'
#     hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
#     emission_probability_via_splitting_exploded(hmm, source_state, sink_state, emissions, emission_index_of_interest, hidden_state_of_interest)





if __name__ == '__main__':
    main()
