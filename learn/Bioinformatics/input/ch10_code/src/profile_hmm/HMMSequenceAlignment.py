from sys import stdin

import yaml

from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_to_dot, \
    to_viterbi_graph, max_product_path_in_viterbi, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, viterbi_to_dot
from profile_hmm.HMMSingleElementAlignment_EmitDelete import ELEM, stringify_probability_keys
from profile_hmm.HMMSingleElementAlignment_InsertMatchDelete import create_hmm_square_from_v_perspective


# MARKDOWN_V_CHAIN
def create_hmm_chain_from_v_perspective(
        v_seq: list[ELEM],
        w_seq: list[ELEM],
        fake_bottom_right_emission_symbol: ELEM
):
    transition_probabilities = {}
    emission_probabilities = {}
    pending = set()
    processed = set()
    hmm_source_n_id = 'S', 0, 0
    fake_bottom_right_emission_symbol_for_square = None
    if 0 == len(v_seq) - 1 and 0 == len(w_seq) - 1:
        fake_bottom_right_emission_symbol_for_square = fake_bottom_right_emission_symbol
    hmm_outgoing_n_ids = create_hmm_square_from_v_perspective(
        transition_probabilities,
        emission_probabilities,
        hmm_source_n_id,
        (0, v_seq[0]),
        (0, w_seq[0]),
        len(v_seq),
        len(w_seq),
        fake_bottom_right_emission_symbol_for_square
    )
    processed.add(hmm_source_n_id)
    pending |= hmm_outgoing_n_ids
    while pending:
        hmm_n_id = pending.pop()
        processed.add(hmm_n_id)
        _, v_idx, w_idx = hmm_n_id
        if v_idx <= len(v_seq) and w_idx <= len(w_seq):
            v_elem = None if v_idx == len(v_seq) else v_seq[v_idx]
            w_elem = None if w_idx == len(w_seq) else w_seq[w_idx]
            fake_bottom_right_emission_symbol_for_square = None
            if v_idx == len(v_seq) - 1 and w_idx == len(w_seq) - 1:
                fake_bottom_right_emission_symbol_for_square = fake_bottom_right_emission_symbol
            hmm_outgoing_n_ids = create_hmm_square_from_v_perspective(
                transition_probabilities,
                emission_probabilities,
                hmm_n_id,
                (v_idx, v_elem),
                (w_idx, w_elem),
                len(v_seq),
                len(w_seq),
                fake_bottom_right_emission_symbol_for_square
            )
            for hmm_test_n_id in hmm_outgoing_n_ids:
                if hmm_test_n_id not in processed:
                    pending.add(hmm_test_n_id)
    return transition_probabilities, emission_probabilities
# MARKDOWN_V_CHAIN


def main_v_chain():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        v_seq = data['v_sequence']
        w_seq = data['w_sequence']
        print(f'Building HMM alignment chain (from v\'s perspective), using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        transition_probabilities, emission_probabilities = create_hmm_chain_from_v_perspective(
            v_seq,
            w_seq,
            '?'
        )
        transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities, emission_probabilities)
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











# MARKDOWN_V_MOST_PROBABLE
def hmm_most_probable_from_v_perspective(
        v_seq: list[ELEM],
        w_seq: list[ELEM],
        t_elem: ELEM,
        transition_probability_overrides: dict[str, dict[str, float]],
        pseudocount: float
):
    transition_probabilities, emission_probabilities = create_hmm_chain_from_v_perspective(v_seq, w_seq, t_elem)
    transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities,
                                                                                  emission_probabilities)
    for hmm_from_n_id in transition_probabilities:
        for hmm_to_n_id in transition_probabilities[hmm_from_n_id]:
            value = 1.0
            if hmm_from_n_id in transition_probability_overrides and \
                    hmm_to_n_id in transition_probability_overrides[hmm_from_n_id]:
                value = transition_probability_overrides[hmm_from_n_id][hmm_to_n_id]
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = value
    hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
    hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm,
        pseudocount
    )
    hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm,
        pseudocount
    )
    hmm_source_n_id = hmm.get_root_node()
    hmm_sink_n_id = 'VITERBI_SINK'  # Fake sink node ID required for exploding HMM into Viterbi graph
    v_seq = v_seq + [t_elem]  # Add fake symbol for when exploding out Viterbi graph
    viterbi = to_viterbi_graph(hmm, hmm_source_n_id, hmm_sink_n_id, v_seq)
    probability, hidden_path = max_product_path_in_viterbi(viterbi)
    v_alignment = []
    # When looping, ignore phony end emission and Viterbi sink node at end: [(T, #, #), VITERBI_SINK].
    for hmm_from_n_id, hmm_to_n_id in hidden_path[:-2]:
        state_type, to_v_idx, to_w_idx = hmm_to_n_id.split(',')
        to_v_idx = int(to_v_idx)
        to_w_idx = int(to_w_idx)
        if state_type == 'D':
            v_alignment.append(None)
        elif state_type in {'M', 'I'}:
            v_alignment.append(v_seq[to_v_idx - 1])
        else:
            raise ValueError('Unrecognizable type')
    return hmm, viterbi, probability, hidden_path, v_alignment
# MARKDOWN_V_MOST_PROBABLE


def main_v_most_probable():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        v_seq = data['v_sequence']
        w_seq = data['w_sequence']
        transition_probability_overrides = data['transition_probability_overrides']
        pseudocount = data['pseudocount']
        print(f'Building HMM alignment chain (from w\'s perspective), using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm, viterbi, weight, hidden_path, v_alignment = hmm_most_probable_from_v_perspective(
            v_seq,
            w_seq,
            '?',
            transition_probability_overrides,
            pseudocount
        )
        print(f'The following HMM was produced AFTER applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        print(f'The following Viterbi graph was produced for the HMM and the emitted sequence {v_seq} ...')
        print()
        print('```{dot}')
        print(f'{viterbi_to_dot(viterbi)}')
        print('```')
        print()
        print()
        print(f'The hidden path with the max product weight in this Viterbi graph is ...')
        print()
        print('```')
        print(f'{"".join("-" if c is None else c for c in v_alignment)}')
        print('```')
        print()
        print(f'Most probable hidden path: {hidden_path}')
        print()
        print(f'Most probable hidden path probability: {weight}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







if __name__ == '__main__':
    main_v_most_probable()
