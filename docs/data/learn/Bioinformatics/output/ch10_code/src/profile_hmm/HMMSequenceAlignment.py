from math import nan
from sys import stdin
from typing import TypeVar

import yaml

from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_to_dot

ELEM = TypeVar('ELEM')


def stringify_probability_keys(transition_probabilities, emission_probabilities):
    def key_to_str(k):
        return ','.join(str(e) for e in k)

    _transition_probabilities = {}
    for k, v in transition_probabilities.items():
        _transition_probabilities[key_to_str(k)] = {}
        for _k, _v in v.items():
            _transition_probabilities[key_to_str(k)][key_to_str(_k)] = _v
    _emission_probabilities = {}
    for k, v in emission_probabilities.items():
        _emission_probabilities[key_to_str(k)] = {}
        for _k, _v in v.items():
            _emission_probabilities[key_to_str(k)][key_to_str(_k)] = _v
    return _transition_probabilities, _emission_probabilities


# MARKDOWN_V_SQUARE
SEQ_HMM_STATE = tuple[str, int, int]


# Transition probabilities set to nan (they should be defined at some point later on).
# Emission probabilities set such that v has a 100% probability of emitting.
def create_hmm_square_from_v_perspective(
        transition_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        emission_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        hmm_top_left_n_id: SEQ_HMM_STATE,
        v_elem: tuple[int, ELEM | None],
        w_elem: tuple[int, ELEM | None],
        v_max_idx: int,
        w_max_idx: int
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
        hmm_to_n_id = 'E', v_idx + 1, w_idx
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][v_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going right (emit), go downward (gap)
        if w_idx < w_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'D', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
            hmm_outgoing_n_ids.add(hmm_to_n_id)
    # From top-left, go downward (gap)
    if w_idx < w_max_idx:
        hmm_to_n_id = 'D', v_idx, w_idx + 1
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going downward (gap), go right (emit)
        if v_idx < v_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
            emission_probabilities[hmm_to_n_id][v_symbol] = 1.0
    # From top-left, go diagonal (emit)
    if v_idx < v_max_idx and w_idx < w_max_idx:
        hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][v_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
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
            1
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












# MARKDOWN_W_SQUARE
# Transition probabilities set to nan (they should be defined at some point later on).
# Emission probabilities set such that v has a 100% probability of emitting.
def create_hmm_square_from_w_perspective(
        transition_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        emission_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        hmm_top_left_n_id: SEQ_HMM_STATE,
        v_elem: tuple[int, ELEM | None],
        w_elem: tuple[int, ELEM | None],
        v_max_idx: int,
        w_max_idx: int
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
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going right (gap), go downward (emit)
        if w_idx < w_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
            emission_probabilities[hmm_to_n_id][w_symbol] = 1.0
            hmm_outgoing_n_ids.add(hmm_to_n_id)
    # From top-left, go downward (emit)
    if w_idx < w_max_idx:
        hmm_to_n_id = 'E', v_idx, w_idx + 1
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][w_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going downward (emit), go right (gap)
        if v_idx < v_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'D', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
    # From top-left, go diagonal (emit)
    if v_idx < v_max_idx and w_idx < w_max_idx:
        hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][w_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
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
            1
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

















# MARKDOWN_V_CHAIN
def create_hmm_chain_from_v_perspective(
        v_seq: list[ELEM],
        w_seq: list[ELEM]
):
    transition_probabilities = {}
    emission_probabilities = {}
    pending = set()
    processed = set()
    hmm_source_n_id = 'S', -1, -1
    hmm_outgoing_n_ids = create_hmm_square_from_v_perspective(
        transition_probabilities,
        emission_probabilities,
        hmm_source_n_id,
        (0, v_seq[0]),
        (0, w_seq[0]),
        len(v_seq),
        len(w_seq)
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
            hmm_outgoing_n_ids = create_hmm_square_from_v_perspective(
                transition_probabilities,
                emission_probabilities,
                hmm_n_id,
                (v_idx, v_elem),
                (w_idx, w_elem),
                len(v_seq),
                len(w_seq)
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
        print(f'Building HMM alignment chain (from w\'s perspective), using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        transition_probabilities, emission_probabilities = create_hmm_chain_from_v_perspective(
            list(v_seq),
            list(w_seq)
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


if __name__ == '__main__':
    main_v_chain()
