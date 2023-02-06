from sys import stdin
from typing import Any

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import HmmNodeData, STATE, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardGraph import filter_at_emission_idx, \
    delete_dead_end_nodes
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import forward_explode_hmm, forward_exploded_hmm_calculation, \
    exploded_to_dot, FORWARD_EXPLODED_NODE_ID, FORWARD_EXPLODED_EDGE_ID


# MARKDOWN
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded = forward_explode_hmm_and_isolate_edge(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq,
                                                      from_emission_idx, from_hidden_state, to_hidden_state)
    # Compute sink weight
    f_exploded_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    return f_exploded, f_exploded_sink_weight


def forward_explode_hmm_and_isolate_edge(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    # Filter starting emission index to edge's starting node.
    f_exploded_keep_from_n_id = from_emission_idx, from_hidden_state
    filter_at_emission_idx(f_exploded, f_exploded_keep_from_n_id)
    # Filter ending emission index to edge's ending node.
    f_exploded_keep_to_n_id = (-1 if to_hidden_state == hmm_sink_n_id else from_emission_idx + 1), to_hidden_state
    filter_at_emission_idx(f_exploded, f_exploded_keep_to_n_id)
    # For the edge's ...
    #  * start node, keep that edge as its only outgoing edge.
    #  * ending node, keep that edge as its only incoming edge.
    for transition in f_exploded.get_outputs(f_exploded_keep_from_n_id):
        _, f_exploded_to_n_id = transition
        if f_exploded_to_n_id != f_exploded_keep_to_n_id:
            f_exploded.delete_edge(transition)
    for transition in f_exploded.get_inputs(f_exploded_keep_to_n_id):
        f_exploded_from_n_id, _ = transition
        if f_exploded_from_n_id != f_exploded_keep_from_n_id:
            f_exploded.delete_edge(transition)
    # By deleting nodes/edges, other nodes may have been orphaned (pointing to dead-ends or starting from dead-ends).
    # Delete those nodes such that there are no dead-ends.
    delete_dead_end_nodes(f_exploded, f_exploded_keep_from_n_id)
    # Return
    return f_exploded
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
        f_exploded, probability = emission_probability(
            hmm,
            source_state,
            sink_state,
            emissions,
            from_emission_idx,
            from_hidden_state,
            to_hidden_state
        )
        print(f'The following isolated exploded HMM was produced -- index  {from_emission_idx} only has the option'
              f' to travel from {from_hidden_state} to {to_hidden_state} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded)}')
        print('```')
        print()
        print(f'The probability of {emissions} being emitted when index {from_emission_idx} only has the option'
              f' to travel from {from_hidden_state} to {to_hidden_state} is {probability}.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
