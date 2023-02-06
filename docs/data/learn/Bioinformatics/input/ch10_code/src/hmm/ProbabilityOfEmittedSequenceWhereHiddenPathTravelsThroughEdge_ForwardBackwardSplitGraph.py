from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardSplitGraph import get_edge_probability
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardSplitGraph import \
    backward_explode, backward_exploded_hmm_calculation
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardSplitGraph import remove_after_node, \
    remove_before_node
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import forward_exploded_hmm_calculation, \
    exploded_to_dot, forward_explode_hmm


# MARKDOWN
def emission_probability_three_split(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    # Forward compute left-hand side
    f_exploded_lhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_from_n_id = from_emission_idx, from_hidden_state
    remove_after_node(f_exploded_lhs, f_exploded_from_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Backward compute right-hand side
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_rhs_to_n_id = (-1 if to_hidden_state == hmm_sink_n_id else from_emission_idx + 1), to_hidden_state
    remove_before_node(f_exploded_rhs, f_exploded_rhs_to_n_id)
    b_exploded_rhs, _ = backward_explode(hmm, f_exploded_rhs)
    b_exploded_rhs_source_weight = backward_exploded_hmm_calculation(hmm, b_exploded_rhs, emitted_seq)
    # Forward compute middle side (this is just the probability of the edge itself)
    _, hmm_from_n_id = f_exploded_from_n_id
    f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_rhs_to_n_id
    f_exploded_middle_sink_weight = get_edge_probability(hmm, hmm_from_n_id, hmm_to_n_id, emitted_seq,
                                                         f_exploded_to_n_emission_idx)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * f_exploded_middle_sink_weight * b_exploded_rhs_source_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (b_exploded_rhs, b_exploded_rhs_source_weight),\
           f_exploded_middle_sink_weight,\
           f_exploded_sink_weight
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
        probability = emission_probability_three_split(
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








if __name__ == '__main__':
    main()
