from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardSplitGraph import \
    backward_explode, backward_exploded_hmm_calculation
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import forward_explode_hmm, forward_exploded_hmm_calculation, \
    exploded_to_dot


# MARKDOWN_SINGLE
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    # Left-hand side forward computation
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    f_exploded_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    f = f_exploded.get_node_data(f_exploded_n_id)
    # Right-hand side backward computation
    b_exploded, b_exploded_n_counter = backward_explode(hmm, f_exploded)
    backward_exploded_hmm_calculation(hmm, b_exploded, emitted_seq)
    b_exploded_n_count = b_exploded_n_counter[f_exploded_n_id] + 1
    b = 0
    for i in range(b_exploded_n_count):
        b_exploded_n_id = f_exploded_n_id, i
        b += b_exploded.get_node_data(b_exploded_n_id)
    # Calculate probability and return
    prob = f * b
    return (f_exploded, f), (b_exploded, b), prob
# MARKDOWN_SINGLE


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
# _, _, a = emission_probability(hmm, 'SOURCE', 'SINK', emitted_seq, 2, 'A')
# _, bg, b = emission_probability(hmm, 'SOURCE', 'SINK', emitted_seq, 2, 'B')
# print(f'{exploded_to_dot(bg)}')
# print(f'{a=} {b=}')
# raise ValueError()
# backward_exploded_hmm_calculation(hmm, exploded, emitted_seq)


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
        print(f' * The left-hand side is computed to have {f_exploded_lhs_prob_sum} at node {hidden_state_of_interest}{emission_idx_of_interest}.')
        print(f' * The right-hand side is is computed to have {b_exploded_rhs_prob_sum} at node(s) {hidden_state_of_interest}{emission_idx_of_interest}.')
        print()
        print(f'When those nodes are multiplied together, its the probability for all hidden paths that travel'
              f' through {hidden_state_of_interest} at index {emission_idx_of_interest} of {emissions}. The probability'
              f' of {emissions} being emitted when index {emission_idx_of_interest} only has the option to emit from'
              f' {hidden_state_of_interest} is {probability}.')
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
    f_exploded_n_ids = set(f_exploded.get_nodes())
    f_exploded_n_ids.remove(f_exploded.get_root_node())
    f_exploded_n_ids.remove(f_exploded.get_leaf_node())
    probs = {}
    for f_exploded_n_id in f_exploded_n_ids:
        f = f_exploded.get_node_data(f_exploded_n_id)
        b_exploded_n_count = b_exploded_n_counter[f_exploded_n_id] + 1
        b = 0
        for i in range(b_exploded_n_count):
            b_exploded_n_id = f_exploded_n_id, i
            b += b_exploded.get_node_data(b_exploded_n_id)
        prob = f * b
        probs[f_exploded_n_id] = prob
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
        for node, prob in sorted(probabilities.items()):
            print(f' * {node} = {prob}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_all()

