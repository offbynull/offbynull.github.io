from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot
from hmm.ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardBackwardFullGraph import \
    all_emission_probabilities
from hmm.ProbabilityOfEmittedSequence_ForwardGraph import exploded_to_dot


# MARKDOWN
def edge_certainties(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL]
):
    f_exploded, b_exploded, filtered_probs = all_emission_probabilities(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_sink_n_id = f_exploded.get_leaf_node()
    unfiltered_prob = f_exploded.get_node_data(f_exploded_sink_n_id)
    certainty = {}
    for f_exploded_n_id, prob in filtered_probs.items():
        certainty[f_exploded_n_id] = prob / unfiltered_prob
    return f_exploded, b_exploded, certainty
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
        f_exploded, b_exploded, certainties = edge_certainties(
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
        print(f'{exploded_to_dot(f_exploded, label="ALL possible left-hand sides (forward)", label_loc="top")}')
        print('```')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(b_exploded, label="ALL possible right-hand sides (backward)", label_loc="top")}')
        print('```')
        print()
        print(f'The **certainty** for {emissions} when the hidden path is limited to traveling through ...')
        print()
        for transition, certainty in sorted(certainties.items()):
            print(f' * {transition[0]} → {transition[1]} = {certainty}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

