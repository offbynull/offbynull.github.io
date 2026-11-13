from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardSplitGraph import get_edge_probability
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardSplitGraph import \
    backward_explode, backward_exploded_hmm_calculation
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import forward_explode_hmm, forward_exploded_hmm_calculation, \
    exploded_to_dot, FORWARD_EXPLODED_NODE_ID


# MARKDOWN_SINGLE
def emission_probability_single(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded_from_n_id = from_emission_idx, from_hidden_state
    f_exploded_to_n_id = (-1 if to_hidden_state == hmm_sink_n_id else from_emission_idx + 1), to_hidden_state
    # Left-hand side forward computation
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    f = f_exploded.get_node_data(f_exploded_from_n_id)
    # Right-hand side backward computation
    b_exploded, b_exploded_n_counter = backward_explode(hmm, f_exploded)
    backward_exploded_hmm_calculation(hmm, b_exploded, emitted_seq)
    b_exploded_n_count = b_exploded_n_counter[f_exploded_to_n_id] + 1
    b = 0
    for i in range(b_exploded_n_count):
        b_exploded_n_id = f_exploded_to_n_id, i
        b += b_exploded.get_node_data(b_exploded_n_id)
    # Forward compute middle side (this is just the probability of the edge itself)
    _, hmm_from_n_id = f_exploded_from_n_id
    f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
    f_exploded_middle_sink_weight = get_edge_probability(hmm, hmm_from_n_id, hmm_to_n_id, emitted_seq,
                                                         f_exploded_to_n_emission_idx)
    # Calculate probability and return
    prob = f * f_exploded_middle_sink_weight * b
    return (f_exploded, f), (b_exploded, b), f_exploded_middle_sink_weight, prob
# MARKDOWN_SINGLE



def main_single():
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
        (f_exploded_lhs, f_exploded_lhs_prob_sum), \
        (b_exploded_rhs, b_exploded_rhs_prob_sum), \
        f_exploded_middle_prob_sum, \
        probability = emission_probability_single(
            hmm,
            source_state,
            sink_state,
            emissions,
            from_emission_idx,
            from_hidden_state,
            to_hidden_state
        )
        print()
        print(f'The following isolated exploded HMM was produced -- index {from_emission_idx} only has the option'
              f' to travel from {from_hidden_state} to {to_hidden_state}, then split based on that *edge*.')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded_lhs, label="Left-hand side", label_loc="top")}')
        print('```')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(b_exploded_rhs, label="Right-hand side (backward)", label_loc="top")}')
        print('```')
        print()
        print(f' * The left-hand side is computed to have {f_exploded_lhs_prob_sum} at its sink node.')
        print(f' * The middle side (the edge itself, not displayed as a graph above) is computed to'
              f' {f_exploded_middle_prob_sum} at its sink node.')
        print(f' * The right-hand side is is computed to have {b_exploded_rhs_prob_sum} at its source node.')
        print()
        print(f'When the sink nodes are multiplied together, its the probability for all hidden paths that travel'
              f' from {from_hidden_state} to {to_hidden_state} at index {from_emission_idx} of {emissions}:'
              f' {probability}.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")




















# MARKDOWN_ALL
def all_emission_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL]
):
    # Left-hand side forward computation
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    # Right-hand side backward computation
    b_exploded, b_exploded_n_counter = backward_explode(hmm, f_exploded)
    backward_exploded_hmm_calculation(hmm, b_exploded, emitted_seq)
    # Calculate ALL probabilities
    probs = {}
    for f_exploded_e_id in f_exploded.get_edges():
        f_exploded_from_n_id, f_exploded_to_n_id = f_exploded_e_id
        # Get node weights
        f = f_exploded.get_node_data(f_exploded_from_n_id)
        b_exploded_n_count = b_exploded_n_counter[f_exploded_to_n_id] + 1
        b = 0
        for i in range(b_exploded_n_count):
            b_exploded_n_id = f_exploded_to_n_id, i
            b += b_exploded.get_node_data(b_exploded_n_id)
        # Get transition probability of edge connecting gap. In certain cases, the SINK node may exist in the HMM. Here
        # we check that the transition exists in the HMM. If it does, we use the transition prob. If it doesn't but it's
        # the SINK node, it's assumed to have a 100% transition probability.
        f_exploded_sink_n_id = f_exploded.get_leaf_node()
        f_exploded_from_n_emissions_idx, hmm_from_n_id = f_exploded_from_n_id
        f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
        f_exploded_middle_sink_weight = get_edge_probability(hmm, hmm_from_n_id, hmm_to_n_id, emitted_seq,
                                                             f_exploded_to_n_emission_idx)
        # Calculate probability and return
        prob = f * f_exploded_middle_sink_weight * b
        probs[f_exploded_e_id] = prob
    return f_exploded, b_exploded, probs
# MARKDOWN_ALL


def main_all():
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
        f_exploded_lhs, b_exploded_rhs, probabilities = all_emission_probabilities(
            hmm,
            source_state,
            sink_state,
            emissions
        )
        print()
        print(f'The fully exploded HMM for the  ...')
        print()
        print(f' * left-hand side was forward computed.')
        print(f' * right-hand side was backward computed.')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded_lhs, label="ALL possible left-hand sides (forward)", label_loc="top")}')
        print('```')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(b_exploded_rhs, label="ALL possible right-hand sides (backward)", label_loc="top")}')
        print('```')
        print()
        print(f'The probability for {emissions} when the hidden path is limited to traveling through ...')
        print()
        for transition, prob in sorted(probabilities.items()):
            print(f' * {transition[0]} → {transition[1]} = {prob}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_all()

