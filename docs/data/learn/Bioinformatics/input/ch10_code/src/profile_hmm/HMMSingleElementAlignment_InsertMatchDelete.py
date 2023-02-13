from sys import stdin

import yaml

from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_to_dot, \
    to_viterbi_graph, max_product_path_in_viterbi, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, viterbi_to_dot
from profile_hmm.HMMSingleElementAlignment_EmitDelete import SEQ_HMM_STATE, ELEM, stringify_probability_keys, \
    inject_emitable, inject_non_emittable


# MARKDOWN_V_SQUARE
def create_hmm_square_from_v_perspective(
        transition_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        emission_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        hmm_top_left_n_id: SEQ_HMM_STATE,
        v_elem: tuple[int, ELEM | None],
        w_elem: tuple[int, ELEM | None],
        v_max_idx: int,
        w_max_idx: int,
        fake_bottom_right_emission_symbol: ELEM | None = None
):
    v_idx, v_symbol = v_elem
    w_idx, w_symbol = w_elem
    hmm_outgoing_n_ids = set()
    # Make sure top-left exists
    if hmm_top_left_n_id not in transition_probabilities:
        transition_probabilities[hmm_top_left_n_id] = {}
        emission_probabilities[hmm_top_left_n_id] = {}
    # From top-left, go right (emit)
    if v_idx < v_max_idx:
        hmm_to_n_id = 'I', v_idx + 1, w_idx
        inject_emitable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            v_symbol,
            hmm_outgoing_n_ids
        )
        # From top-left, after going right (emit), go downward (gap)
        if w_idx < w_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'D', v_idx + 1, w_idx + 1
            inject_non_emittable(
                transition_probabilities,
                emission_probabilities,
                hmm_from_n_id,
                hmm_to_n_id,
                hmm_outgoing_n_ids
            )
    # From top-left, go downward (gap)
    if w_idx < w_max_idx:
        hmm_to_n_id = 'D', v_idx, w_idx + 1
        inject_non_emittable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            hmm_outgoing_n_ids
        )
        # From top-left, after going downward (gap), go right (emit)
        if v_idx < v_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'I', v_idx + 1, w_idx + 1
            inject_emitable(
                transition_probabilities,
                emission_probabilities,
                hmm_from_n_id,
                hmm_to_n_id,
                v_symbol,
                hmm_outgoing_n_ids
            )
    # From top-left, go diagonal (emit)
    if v_idx < v_max_idx and w_idx < w_max_idx:
        hmm_to_n_id = 'M', v_idx + 1, w_idx + 1
        inject_emitable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            v_symbol,
            hmm_outgoing_n_ids
        )
    # Add fake bottom-right emission (if it's been asked for)
    if fake_bottom_right_emission_symbol is not None:
        hmm_bottom_right_n_id_final = 'T', v_idx + 1, w_idx + 1
        hmm_bottom_right_n_ids = {
            ('M', v_idx + 1, w_idx + 1),
            ('D', v_idx + 1, w_idx + 1),
            ('I', v_idx + 1, w_idx + 1)
        }
        for hmm_bottom_right_n_id in hmm_bottom_right_n_ids:
            if hmm_bottom_right_n_id in hmm_outgoing_n_ids:
                inject_emitable(
                    transition_probabilities,
                    emission_probabilities,
                    hmm_bottom_right_n_id,
                    hmm_bottom_right_n_id_final,
                    fake_bottom_right_emission_symbol,
                    hmm_outgoing_n_ids
                )
                hmm_outgoing_n_ids.remove(hmm_bottom_right_n_id)
    # Return
    return hmm_outgoing_n_ids
# MARKDOWN_V_SQUARE


def main_v_square():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        v_elem = data['v_element']
        w_elem = data['w_element']
        print(f'Building HMM alignment square (from v\'s perspective), using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        transition_probabilities = {}
        emission_probabilities = {}
        create_hmm_square_from_v_perspective(
            transition_probabilities,
            emission_probabilities,
            ('S', -1, -1),
            (0, v_elem),
            (0, w_elem),
            1,
            1,
            '?'
        )
        transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities, emission_probabilities)
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced (all transition weights set to NaN) ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")












# MARKDOWN_W_SQUARE
def create_hmm_square_from_w_perspective(
        transition_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        emission_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        hmm_top_left_n_id: SEQ_HMM_STATE,
        v_elem: tuple[int, ELEM | None],
        w_elem: tuple[int, ELEM | None],
        v_max_idx: int,
        w_max_idx: int,
        fake_bottom_right_emission_symbol: ELEM | None = None
):
    v_idx, v_symbol = v_elem
    w_idx, w_symbol = w_elem
    hmm_outgoing_n_ids = set()
    # Make sure top-left exists
    if hmm_top_left_n_id not in transition_probabilities:
        transition_probabilities[hmm_top_left_n_id] = {}
        emission_probabilities[hmm_top_left_n_id] = {}
    # From top-left, go right (gap)
    if v_idx < v_max_idx:
        hmm_to_n_id = 'D', v_idx + 1, w_idx
        inject_non_emittable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            hmm_outgoing_n_ids
        )
        # From top-left, after going right (gap), go downward (emit)
        if w_idx < w_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'I', v_idx + 1, w_idx + 1
            inject_emitable(
                transition_probabilities,
                emission_probabilities,
                hmm_from_n_id,
                hmm_to_n_id,
                w_symbol,
                hmm_outgoing_n_ids
            )
    # From top-left, go downward (emit)
    if w_idx < w_max_idx:
        hmm_to_n_id = 'I', v_idx, w_idx + 1
        inject_emitable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            w_symbol,
            hmm_outgoing_n_ids
        )
        # From top-left, after going downward (emit), go right (gap)
        if v_idx < v_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'D', v_idx + 1, w_idx + 1
            inject_non_emittable(
                transition_probabilities,
                emission_probabilities,
                hmm_from_n_id,
                hmm_to_n_id,
                hmm_outgoing_n_ids
            )
    # From top-left, go diagonal (emit)
    if v_idx < v_max_idx and w_idx < w_max_idx:
        hmm_to_n_id = 'M', v_idx + 1, w_idx + 1
        inject_emitable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            w_symbol,
            hmm_outgoing_n_ids
        )
    # Add fake bottom-right emission (if it's been asked for)
    if fake_bottom_right_emission_symbol is not None:
        hmm_bottom_right_n_id_final = 'T', v_idx + 1, w_idx + 1
        hmm_bottom_right_n_ids = {
            ('M', v_idx + 1, w_idx + 1),
            ('D', v_idx + 1, w_idx + 1),
            ('I', v_idx + 1, w_idx + 1)
        }
        for hmm_bottom_right_n_id in hmm_bottom_right_n_ids:
            if hmm_bottom_right_n_id in hmm_outgoing_n_ids:
                inject_emitable(
                    transition_probabilities,
                    emission_probabilities,
                    hmm_bottom_right_n_id,
                    hmm_bottom_right_n_id_final,
                    fake_bottom_right_emission_symbol,
                    hmm_outgoing_n_ids
                )
                hmm_outgoing_n_ids.remove(hmm_bottom_right_n_id)
    # Return
    return hmm_outgoing_n_ids
# MARKDOWN_W_SQUARE


def main_w_square():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        v_elem = data['v_element']
        w_elem = data['w_element']
        print(f'Building HMM alignment square (from w\'s perspective), using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        transition_probabilities = {}
        emission_probabilities = {}
        create_hmm_square_from_w_perspective(
            transition_probabilities,
            emission_probabilities,
            ('S', -1, -1),
            (0, v_elem),
            (0, w_elem),
            1,
            1,
            '?'
        )
        transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities, emission_probabilities)
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced (all transition weights set to NaN) ...')
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
        v_elem: ELEM,
        w_elem: ELEM,
        t_elem: ELEM,
        transition_probability_overrides: dict[str, dict[str, float]],
        pseudocount: float
):
    transition_probabilities = {}
    emission_probabilities = {}
    create_hmm_square_from_v_perspective(
        transition_probabilities,
        emission_probabilities,
        ('S', -1, -1),
        (0, v_elem),
        (0, w_elem),
        1,
        1,
        t_elem
    )
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
    viterbi = to_viterbi_graph(hmm, hmm_source_n_id, hmm_sink_n_id, [v_elem] + [t_elem])
    probability, hidden_path = max_product_path_in_viterbi(viterbi)
    v_alignment = []
    # When looping, ignore phony end emission and Viterbi sink node at end: [(T, 1, 1), VITERBI_SINK].
    for hmm_from_n_id, hmm_to_n_id in hidden_path[:-2]:
        state_type, to_v_idx, to_w_idx = hmm_to_n_id.split(',')
        if state_type == 'D':
            v_alignment.append(None)
        elif state_type in {'M', 'I'}:
            v_alignment.append(v_elem)
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
        v_seq = data['v_element']
        w_seq = data['w_element']
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
