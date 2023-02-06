from collections import Counter
from sys import stdin
from typing import Any

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardSplitGraph import remove_after_node, \
    remove_before_node
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import forward_explode_hmm, forward_exploded_hmm_calculation, \
    exploded_to_dot, FORWARD_EXPLODED_NODE_ID, FORWARD_EXPLODED_EDGE_ID

# MARKDOWN_BACKWARD_EXPLODE
BACKWARD_EXPLODED_NODE_ID = tuple[FORWARD_EXPLODED_NODE_ID, int]
BACKWARD_EXPLODED_EDGE_ID = tuple[BACKWARD_EXPLODED_NODE_ID, BACKWARD_EXPLODED_NODE_ID]


def backward_explode(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any]
):
    f_exploded_source_n_id = f_exploded.get_root_node()
    f_exploded_sink_n_id = f_exploded.get_leaf_node()
    # Copy forward graph in the style of the backward graph
    b_exploded = Graph()
    for f_exploded_id in f_exploded.get_nodes():
        b_exploded_n_id = f_exploded_id, 0
        b_exploded.insert_node(b_exploded_n_id)
    for f_exploded_transition in f_exploded.get_edges():
        f_exploded_from_n_id, f_exploded_to_n_id = f_exploded_transition
        b_exploded_from_n_id = f_exploded_from_n_id, 0
        b_exploded_to_n_id = f_exploded_to_n_id, 0
        b_exploded_transition = b_exploded_from_n_id, b_exploded_to_n_id
        b_exploded.insert_edge(
            b_exploded_transition,
            b_exploded_from_n_id,
            b_exploded_to_n_id
        )
    # Duplicate nodes in backward graph based on transitions to non-emitting states
    b_exploded_n_counter = Counter()
    b_exploded_source_n_id = f_exploded_source_n_id, 0
    ready_set = {b_exploded_source_n_id}
    waiting_set = {}
    while ready_set:
        b_exploded_from_n_id = ready_set.pop()
        b_exploded_duplicated_from_n_ids = backward_exploded_duplicate_outwards(
            hmm,
            f_exploded_source_n_id,
            f_exploded_sink_n_id,
            b_exploded_from_n_id,
            b_exploded,
            b_exploded_n_counter
        )
        ready_set |= b_exploded_duplicated_from_n_ids
        for _, _, b_exploded_to_n_id, _ in b_exploded.get_outputs_full(b_exploded_from_n_id):
            if b_exploded_to_n_id not in waiting_set:
                waiting_set[b_exploded_to_n_id] = b_exploded.get_in_degree(b_exploded_to_n_id)
            waiting_set[b_exploded_to_n_id] -= 1
            if waiting_set[b_exploded_to_n_id] == 0:
                del waiting_set[b_exploded_to_n_id]
                ready_set.add(b_exploded_to_n_id)
    return b_exploded, b_exploded_n_counter


def backward_exploded_duplicate_outwards(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_source_n_id: FORWARD_EXPLODED_NODE_ID,
        f_exploded_sink_n_id: FORWARD_EXPLODED_NODE_ID,
        b_exploded_n_id: BACKWARD_EXPLODED_NODE_ID,
        b_exploded: Graph[BACKWARD_EXPLODED_NODE_ID, Any, BACKWARD_EXPLODED_EDGE_ID, Any],
        b_exploded_n_counter: Counter[FORWARD_EXPLODED_NODE_ID]
):
    # We're splitting based on outgoing edges -- if there's only a single outgoing edge, there's no point in trying to
    # split anything
    if b_exploded.get_out_degree(b_exploded_n_id) == 1:
        return set()
    f_exploded_n_id, _ = b_exploded_n_id
    # Source node shouldn't get duplicated
    if f_exploded_n_id == f_exploded_source_n_id:
        return set()
    b_exploded_new_n_ids = set()
    for _, _, b_exploded_to_n_id, _ in set(b_exploded.get_outputs_full(b_exploded_n_id)):
        f_exploded_to_n_id, _, = b_exploded_to_n_id
        _, hmm_to_n_id = f_exploded_to_n_id
        if f_exploded_to_n_id != f_exploded_sink_n_id and not hmm.get_node_data(hmm_to_n_id).is_emittable():
            b_exploded_n_counter[f_exploded_n_id] += 1
            b_exploded_new_n_count = b_exploded_n_counter[f_exploded_n_id]
            b_exploded_new_n_id = f_exploded_n_id, b_exploded_new_n_count
            b_exploded.insert_node(b_exploded_new_n_id)
            b_old_transition = b_exploded_n_id, b_exploded_to_n_id
            b_exploded.delete_edge(b_old_transition)
            b_new_transition = b_exploded_new_n_id, b_exploded_to_n_id
            b_exploded.insert_edge(
                b_new_transition,
                b_exploded_new_n_id,
                b_exploded_to_n_id
            )
            b_exploded_new_n_ids.add(b_exploded_new_n_id)
    for _, b_exploded_from_n_id, _, _ in b_exploded.get_inputs_full(b_exploded_n_id):
        for b_exploded_new_n_id in b_exploded_new_n_ids:
            b_new_transition = b_exploded_from_n_id, b_exploded_new_n_id
            b_exploded.insert_edge(
                b_new_transition,
                b_exploded_from_n_id,
                b_exploded_new_n_id
            )
    return b_exploded_new_n_ids
# MARKDOWN_BACKWARD_EXPLODE


def main_backward_explode():
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
        print(f'Generate a backwards graph of an HMM emitting a sequence, using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        f_exploded_lhs = forward_explode_hmm(hmm, source_state, sink_state, emissions)
        print(f'The following forward exploded HMM was produced for the HMM and the emitted sequence {emissions} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded_lhs, label="Forward graph", label_loc="top")}')
        print('```')
        print()
        b_exploded_rhs, _ = backward_explode(hmm, f_exploded_lhs)
        print(f'The following backward exploded HMM was produced for the HMM and the emitted sequence {emissions} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(b_exploded_rhs, label="Backward graph", label_loc="top")}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")












































# MARKDOWN_FORWARD_BACKWARD_SPLIT
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
    remove_after_node(f_exploded_lhs, f_exploded_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Isolate right-hand side and compute BACKWARDS
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    remove_before_node(f_exploded_rhs, f_exploded_n_id)
    b_exploded_rhs, _ = backward_explode(hmm, f_exploded_rhs)
    b_exploded_rhs_source_weight = backward_exploded_hmm_calculation(hmm, b_exploded_rhs, emitted_seq)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * b_exploded_rhs_source_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (b_exploded_rhs, b_exploded_rhs_source_weight),\
           f_exploded_sink_weight


def backward_exploded_hmm_calculation(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        b_exploded: Graph[BACKWARD_EXPLODED_NODE_ID, Any, BACKWARD_EXPLODED_EDGE_ID, Any],
        emitted_seq: list[SYMBOL]
):
    b_exploded_source_n_id = b_exploded.get_root_node()
    b_exploded_sink_n_id = b_exploded.get_leaf_node()
    (b_exploded_sink_n_emissions_idx, hmm_sink_n_id), _ = b_exploded_sink_n_id
    b_exploded.update_node_data(b_exploded_sink_n_id, 1.0)
    b_exploded_from_n_ids = set()
    add_ready_to_process_incoming_nodes(b_exploded, b_exploded_sink_n_id, b_exploded_from_n_ids)
    while b_exploded_from_n_ids:
        b_exploded_from_n_id = b_exploded_from_n_ids.pop()
        (_, hmm_from_n_id), _ = b_exploded_from_n_id
        b_exploded_from_backward_weight = 0.0
        for _, _, b_exploded_to_n_id, _ in b_exploded.get_outputs_full(b_exploded_from_n_id):
            b_exploded_to_backward_weight = b_exploded.get_node_data(b_exploded_to_n_id)
            (b_exploded_to_n_emissions_idx, hmm_to_n_id), _ = b_exploded_to_n_id
            # Determine symbol emission prob.
            symbol = emitted_seq[b_exploded_to_n_emissions_idx]
            if hmm.has_node(hmm_to_n_id) and hmm.get_node_data(hmm_to_n_id).is_emittable():
                symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol)
            else:
                symbol_emission_prob = 1.0  # No emission - setting to 1.0 means it has no effect in multiply later on
            # Determine transition prob.
            transition = hmm_from_n_id, hmm_to_n_id
            if hmm.has_edge(transition):
                transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            else:
                transition_prob = 1.0  # Setting to 1.0 means it always happens
            b_exploded_from_backward_weight += b_exploded_to_backward_weight * transition_prob * symbol_emission_prob
        b_exploded.update_node_data(b_exploded_from_n_id, b_exploded_from_backward_weight)
        add_ready_to_process_incoming_nodes(b_exploded, b_exploded_from_n_id, b_exploded_from_n_ids)
    return b_exploded.get_node_data(b_exploded_source_n_id)


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_incoming_nodes(
        backward_exploded: Graph[BACKWARD_EXPLODED_NODE_ID, Any, BACKWARD_EXPLODED_EDGE_ID, Any],
        backward_exploded_n_from_id: BACKWARD_EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[BACKWARD_EXPLODED_NODE_ID]
):
    for _, exploded_from_n_id, _, _ in backward_exploded.get_inputs_full(backward_exploded_n_from_id):
        ready_to_process = all(backward_exploded.get_node_data(n) is not None for _, _, n, _ in backward_exploded.get_outputs_full(exploded_from_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_from_n_id)
# MARKDOWN_FORWARD_BACKWARD_SPLIT


# hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(
#     # {
#     #     'SOURCE': {'A': 0.5, 'B': 0.5},
#     #     'A': {'A': 0.911, 'B': 0.089},
#     #     'B': {'A': 0.228, 'B': 0.772},
#     # },
#     # {
#     #     'SOURCE': {},
#     #     'A': {'x': 0.356, 'y': 0.191, 'z': 0.453},
#     #     'B': {'x': 0.040, 'y': 0.467, 'z': 0.493},
#     # }
#     {
#         'SOURCE': {'A': 0.5, 'B': 0.5},
#         'A': {'A': 0.377, 'B': 0.623},
#         'B': {'A': 0.301, 'C': 0.699},
#         'C': {'B': 1.0}
#     },
#     {
#         'SOURCE': {},
#         'A': {'x': 0.176, 'y': 0.596, 'z': 0.228},
#         'B': {'x': 0.225, 'y': 0.572, 'z': 0.203},
#         'C': {}
#     }
# )
# # emitted_seq = list('zyxxxxyxzz')
# emitted_seq = list('zzy')
# exploded = explode_hmm(hmm, 'SOURCE', 'SINK', emitted_seq)
# forward_remove_before(exploded, hmm, 'SOURCE', 'SINK', 1, 'B')
# backward_exploded = backward_explode(hmm, exploded)
# backward_exploded_hmm_calculation(hmm, backward_exploded, emitted_seq)
# print(f'{exploded_to_dot(backward_exploded)}')
# raise ValueError()



def main_forward_backward_split():
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
        (b_exploded_rhs, b_exploded_rhs_prob_sum), \
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
              f' {hidden_state_of_interest}, then split based on that node where the ...')
        print()
        print(f' * left-hand side was forward computed.')
        print(f' * right-hand side was backward computed.')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded_lhs, label="Left-hand side (forward)", label_loc="top")}')
        print('```')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(b_exploded_rhs, label="Right-hand side (backward)", label_loc="top")}')
        print('```')
        print()
        print(f' * The left-hand side is computed to have {f_exploded_lhs_prob_sum} at its sink node.')
        print(f' * The right-hand side is is computed to have {b_exploded_rhs_prob_sum} at its source node.')
        print()
        print(f'When those nodes are multiplied together, its the probability for all hidden paths that travel'
              f' through {hidden_state_of_interest} at index {emission_idx_of_interest} of {emissions}. The probability'
              f' of {emissions} being emitted when index {emission_idx_of_interest} only has the option to emit from'
              f' {hidden_state_of_interest} is {probability}.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_forward_backward_split()
