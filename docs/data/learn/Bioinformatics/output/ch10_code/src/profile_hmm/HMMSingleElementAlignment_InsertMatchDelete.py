import math
from math import nan
from random import random
from sys import stdin
from typing import TypeVar

import yaml

from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_to_dot, \
    to_viterbi_graph, max_product_path_in_viterbi, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, viterbi_to_dot
from profile_hmm import HMMSingleElementAlignment_EmitDelete
from profile_hmm.HMMSingleElementAlignment_EmitDelete import SEQ_HMM_STATE, ELEM, stringify_probability_keys


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
    hmm_outgoing_n_ids = HMMSingleElementAlignment_EmitDelete.create_hmm_square_from_v_perspective(
        transition_probabilities,
        emission_probabilities,
        hmm_top_left_n_id,
        v_elem,
        w_elem,
        v_max_idx,
        w_max_idx,
        fake_bottom_right_emission_symbol
    )
    v_idx, v_symbol = v_elem
    w_idx, w_symbol = w_elem
    # Remove E10
    hmm_remove_n_id = 'E', v_idx + 1, w_idx
    if hmm_remove_n_id in transition_probabilities:
        removed_ep = emission_probabilities.pop(hmm_remove_n_id)
        removed_tp = transition_probabilities.pop(hmm_remove_n_id)
        if hmm_remove_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.remove(hmm_remove_n_id)
        # Replace with I10
        hmm_replace_match_n_id = 'I', v_idx + 1, w_idx
        transition_probabilities[hmm_replace_match_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_match_n_id] = removed_ep.copy()
        transition_probabilities[hmm_top_left_n_id][hmm_replace_match_n_id] = transition_probabilities[hmm_top_left_n_id].pop(hmm_remove_n_id)
        if hmm_replace_match_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.add(hmm_replace_match_n_id)
    # Remove E11
    hmm_remove_n_id = 'E', v_idx + 1, w_idx + 1
    if hmm_remove_n_id in transition_probabilities:
        removed_ep = emission_probabilities.pop(hmm_remove_n_id)
        removed_tp = transition_probabilities.pop(hmm_remove_n_id)
        if hmm_remove_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.remove(hmm_remove_n_id)
        # Replace with M11
        hmm_replace_match_n_id = 'M', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_replace_match_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_match_n_id] = removed_ep.copy()
        transition_probabilities[hmm_top_left_n_id][hmm_replace_match_n_id] = transition_probabilities[hmm_top_left_n_id].pop(hmm_remove_n_id)
        if hmm_replace_match_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.add(hmm_replace_match_n_id)
        # Replace with I11
        hmm_bottom_left_n_id = 'D', v_idx, w_idx + 1
        hmm_replace_insert_n_id = 'I', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_replace_insert_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_insert_n_id] = removed_ep.copy()
        transition_probabilities[hmm_bottom_left_n_id][hmm_replace_insert_n_id] = transition_probabilities[hmm_bottom_left_n_id].pop(hmm_remove_n_id)
        if hmm_replace_insert_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.add(hmm_replace_insert_n_id)
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
    hmm_outgoing_n_ids = HMMSingleElementAlignment_EmitDelete.create_hmm_square_from_w_perspective(
        transition_probabilities,
        emission_probabilities,
        hmm_top_left_n_id,
        v_elem,
        w_elem,
        v_max_idx,
        w_max_idx,
        fake_bottom_right_emission_symbol
    )
    v_idx, v_symbol = v_elem
    w_idx, w_symbol = w_elem
    # Remove E01
    hmm_remove_n_id = 'E', v_idx, w_idx + 1
    if hmm_remove_n_id in transition_probabilities:
        removed_ep = emission_probabilities.pop(hmm_remove_n_id)
        removed_tp = transition_probabilities.pop(hmm_remove_n_id)
        if hmm_remove_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.remove(hmm_remove_n_id)
        # Replace with I01
        hmm_replace_match_n_id = 'I', v_idx, w_idx + 1
        transition_probabilities[hmm_replace_match_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_match_n_id] = removed_ep.copy()
        transition_probabilities[hmm_top_left_n_id][hmm_replace_match_n_id] = transition_probabilities[
            hmm_top_left_n_id].pop(hmm_remove_n_id)
        if hmm_replace_match_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.add(hmm_replace_match_n_id)
    # Remove E11
    hmm_remove_n_id = 'E', v_idx + 1, w_idx + 1
    if hmm_remove_n_id in transition_probabilities:
        removed_ep = emission_probabilities.pop(hmm_remove_n_id)
        removed_tp = transition_probabilities.pop(hmm_remove_n_id)
        if hmm_remove_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.remove(hmm_remove_n_id)
        # Replace with M11
        hmm_replace_match_n_id = 'M', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_replace_match_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_match_n_id] = removed_ep.copy()
        transition_probabilities[hmm_top_left_n_id][hmm_replace_match_n_id] = transition_probabilities[
            hmm_top_left_n_id].pop(hmm_remove_n_id)
        if hmm_replace_match_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.add(hmm_replace_match_n_id)
        # Replace with I11
        hmm_bottom_left_n_id = 'D', v_idx + 1, w_idx
        hmm_replace_insert_n_id = 'I', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_replace_insert_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_insert_n_id] = removed_ep.copy()
        transition_probabilities[hmm_bottom_left_n_id][hmm_replace_insert_n_id] = transition_probabilities[
            hmm_bottom_left_n_id].pop(hmm_remove_n_id)
        if hmm_replace_insert_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.add(hmm_replace_insert_n_id)
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
        elif state_type == 'E':
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
    main_w_square()
