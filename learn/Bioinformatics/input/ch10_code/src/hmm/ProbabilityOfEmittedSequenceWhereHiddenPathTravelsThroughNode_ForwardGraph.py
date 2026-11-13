from sys import stdin
from typing import Any

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import HmmNodeData, STATE, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import forward_explode_hmm, forward_exploded_hmm_calculation, \
    exploded_to_dot, FORWARD_EXPLODED_NODE_ID, FORWARD_EXPLODED_EDGE_ID


# MARKDOWN
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_keep_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    filter_at_emission_idx(f_exploded, f_exploded_keep_n_id)
    f_exploded_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    return f_exploded, f_exploded_sink_weight


def filter_at_emission_idx(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    f_exploded_keep_n_emission_idx, _ = f_exploded_keep_n_id
    f_exploded_keep_n_ids = get_connected_nodes_at_emission_idx(f_exploded, f_exploded_keep_n_id)
    for f_exploded_test_n_id in set(f_exploded.get_nodes()):
        f_exploded_test_n_emission_idx, _ = f_exploded_test_n_id
        if f_exploded_test_n_emission_idx == f_exploded_keep_n_emission_idx\
                and f_exploded_test_n_id not in f_exploded_keep_n_ids:
            f_exploded.delete_node(f_exploded_test_n_id)
    # By deleting nodes above, other nodes may have been orphaned (pointing to dead-ends or starting from dead-ends).
    # Delete those nodes such that there are no dead-ends.
    delete_dead_end_nodes(f_exploded, f_exploded_keep_n_id)


def get_connected_nodes_at_emission_idx(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    f_exploded_keep_n_emission_idx, _ = f_exploded_keep_n_id
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_id):
            f_exploded_to_n_emission_idx, _ = f_exploded_to_n_id
            if f_exploded_keep_n_emission_idx == f_exploded_to_n_emission_idx and f_exploded_to_n_id not in visited:
                visited.add(f_exploded_to_n_id)
        for _, f_exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_n_id):
            f_exploded_from_n_emission_idx, _ = f_exploded_from_n_id
            if f_exploded_keep_n_emission_idx == f_exploded_from_n_emission_idx and f_exploded_from_n_id not in visited:
                visited.add(f_exploded_from_n_id)
    return visited


def delete_dead_end_nodes(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    # Walk backwards to source
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, f_exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_n_id):
            if f_exploded_from_n_id not in visited:
                pending.add(f_exploded_from_n_id)
    backward_visited = visited
    # Walk forward to sink
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_id):
            if f_exploded_to_n_id not in visited:
                pending.add(f_exploded_to_n_id)
    forward_visited = visited
    # Remove anything that wasn't touched (these are dead-ends)
    visited = backward_visited | forward_visited
    for f_exploded_n_id in set(f_exploded.get_nodes()):
        if f_exploded_n_id not in visited:
            f_exploded.delete_node(f_exploded_n_id)
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
        f_exploded, probability = emission_probability(
            hmm,
            source_state,
            sink_state,
            emissions,
            emission_idx_of_interest,
            hidden_state_of_interest
        )
        print(f'The following isolated exploded HMM was produced -- index {emission_idx_of_interest} only has the'
              f' option to travel through {hidden_state_of_interest} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded)}')
        print('```')
        print()
        print(f'The probability of {emissions} being emitted when index {emission_idx_of_interest} only has the option'
              f' to emit from {hidden_state_of_interest} is {probability}.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
