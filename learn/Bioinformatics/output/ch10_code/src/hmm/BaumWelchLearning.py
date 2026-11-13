import math
from collections import defaultdict
from random import random
from sys import stdin
from typing import Generator

import yaml

from graph.DirectedGraph import Graph
from hmm.CertaintyOfEmittedSequenceTravelingThroughHiddenPathEdge import edge_certainties
from hmm.CertaintyOfEmittedSequenceTravelingThroughHiddenPathNode import node_certainties
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_to_dot, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities


# MARKDOWN
from hmm.ViterbiLearning import randomize_hmm_probabilities


def baum_welch_learning(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        pseudocount: float,
        cycles: int
) -> Generator[
    tuple[
        Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        dict[tuple[STATE, STATE], float],
        dict[tuple[STATE, SYMBOL], float]
    ],
    None,
    None
]:
    for _ in range(cycles):
        transition_probs = edge_certainties_to_transition_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq)
        emission_probs = node_certainties_to_emission_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq)
        # Apply new probabilities
        for (hmm_from_n_id, hmm_to_n_id), prob in transition_probs.items():
            transition = hmm_from_n_id, hmm_to_n_id
            hmm.get_edge_data(transition).set_transition_probability(prob)
        for (hmm_to_n_id, symbol), prob in emission_probs.items():
            hmm.get_node_data(hmm_to_n_id).set_symbol_emission_probability(symbol, prob)
        # Apply pseudocounts to new probabilities
        hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
            hmm,
            pseudocount
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount
        )
        # Yield
        yield hmm, transition_probs, emission_probs
# MARKDOWN


# MARKDOWN_NODE
def node_certainties_to_emission_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq):
    _, _, f_exploded_n_certainties = node_certainties(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    # Sum up emission certainties. Everytime the hidden state N emits C, its certainty gets added to ...
    #  * summed_emission_certainties[N, C]           - groups by (N,C) and sums each group
    #  * summed_emission_certainties_by_to_state[N]  - groups by N and sums each group
    summed_emission_certainties = defaultdict(lambda: 0.0)
    summed_emission_certainties_by_to_state = defaultdict(lambda: 0.0)
    for f_exploded_to_n_id, certainty in f_exploded_n_certainties.items():
        f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
        # if hmm_to_n_id == hmm_source_n_id or hmm_to_n_id == hmm_sink_n_id:
        #     continue
        symbol = emitted_seq[f_exploded_to_n_emission_idx]
        summed_emission_certainties[hmm_to_n_id, symbol] += certainty
        summed_emission_certainties_by_to_state[hmm_to_n_id] += certainty
    # Calculate new emission probabilities:
    # For each emission in the HMM (N,C), set that emission's probability using the certainty sums.
    # Specifically, the sum of certainties for (N,C) divided by the sum of all certainties from N.
    emission_probs = defaultdict(lambda: 0.0)
    for hmm_to_n_id, symbol in summed_emission_certainties:
        portion = summed_emission_certainties[hmm_to_n_id, symbol]
        total = summed_emission_certainties_by_to_state[hmm_to_n_id]
        emission_probs[hmm_to_n_id, symbol] = portion / total
    return emission_probs
# MARKDOWN_NODE


# MARKDOWN_EDGE
def edge_certainties_to_transition_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq):
    _, _, f_exploded_e_certainties = edge_certainties(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    # Sum up transition certainties. Everytime the transition S->E is encountered, its certainty gets added to ...
    #  * summed_transition_certainties[S, E]             - groups by (S,E) and sums each group
    #  * summed_transition_certainties_by_from_state[S]  - groups by S and sums each group
    summed_transition_certainties = defaultdict(lambda: 0.0)
    summed_transition_certainties_by_from_state = defaultdict(lambda: 0.0)
    for (f_exploded_from_n_id, f_exploded_to_n_id), certainty in f_exploded_e_certainties.items():
        _, hmm_from_n_id = f_exploded_from_n_id
        _, hmm_to_n_id = f_exploded_to_n_id
        # Sink node may not exist in the HMM. The check below tests for that and skips if it doesn't exist.
        transition = hmm_from_n_id, hmm_to_n_id
        if not hmm.has_edge(transition):
            continue
        summed_transition_certainties[hmm_from_n_id, hmm_to_n_id] += certainty
        summed_transition_certainties_by_from_state[hmm_from_n_id] += certainty
    # Calculate new transition probabilities:
    # For each transition in the HMM (S,E), set that transition's probability using the certainty sums.
    # Specifically, the sum of certainties for (S,E) divided by the sum of all certainties starting from S.
    transition_probs = defaultdict(lambda: 0.0)
    for hmm_from_n_id, hmm_to_n_id in summed_transition_certainties:
        portion = summed_transition_certainties[hmm_from_n_id, hmm_to_n_id]
        total = summed_transition_certainties_by_from_state[hmm_from_n_id]
        transition_probs[hmm_from_n_id, hmm_to_n_id] = portion / total
    return transition_probs
# MARKDOWN_EDGE


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transitions = {k: set(v) for k, v in data['transitions'].items()}
        emissions = {k: set(v) for k, v in data['emissions'].items()}
        source_state = data['source_state']
        sink_state = data['sink_state']
        emission_seq = data['emission_seq']
        cycles = data['cycles']
        pseudocount = data['pseudocount']
        print(f'Deriving HMM probabilities using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        transition_probs = {}
        for src, dsts in transitions.items():
            transition_probs[src] = {dst: math.nan for dst in dsts}
        emission_probs = {}
        for src, syms in emissions.items():
            emission_probs[src] = {sym: math.nan for sym in syms}
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs)
        print(f'The following HMM was produced (no probabilities) ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        randomize_hmm_probabilities(hmm)
        print(f'The following HMM was produced after applying randomized probabilities ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        print(f'Applying Baum-Welch learning for {cycles} cycles ...')
        print()
        for hmm, transition_probs, emission_probs in baum_welch_learning(hmm, source_state, sink_state, emission_seq, pseudocount, cycles):
            print(f' 1. New transition probabilities:')
            for (from_state, to_state), prob in transition_probs.items():
                print(f'    * {from_state}→{to_state} = {prob}')
            print()
            print(f'    New emission probabilities:')
            for (to_state, to_symbol), prob in emission_probs.items():
                print(f'    * ({to_state}, {to_symbol}) = {prob}')
            print()
        print()
        print(f'The following HMM was produced after Baum-Welch learning was applied for {cycles} cycles ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
