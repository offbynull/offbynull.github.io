from collections import defaultdict
from itertools import product
from typing import TypeVar

from graph.DirectedGraph import Graph
from helpers.Utils import slide_window, unique_id_generator

ELEM = TypeVar('ELEM')


def filter_unstable_columns(
        alignment: list[list[ELEM | None]],
        column_removal_threshold: float
) -> list[int]:
    # Accordingly, biologists often ignore columns for which the fraction of space symbols is greater than or equal to a
    # column removal threshold θ
    rows = len(alignment)
    cols = len(alignment[0])
    keep_cols = []
    for i in range(cols):
        missing = 0
        for seq in alignment:
            if seq[i] is None:
                missing += 1
        missing_percentage = missing / rows
        if missing_percentage >= column_removal_threshold:
            continue
        keep_cols.append(i)
    return keep_cols


def alignment_profile(
        alignment: list[list[ELEM | None]],
        symbols: set[ELEM]
):
    cols = len(alignment[0])
    profile = []
    for i in range(cols):
        col_counts = {s: 0 for s in symbols}
        col_total = 0
        for seq in alignment:
            symbol = seq[i]
            if symbol is None:
                continue
            col_counts[symbol] += 1
            col_total += 1
        col_symbol_profile = {s: c / col_total for s, c in col_counts.items()}
        profile.append(col_symbol_profile)
    return profile
















def alignment_to_hmm(
        v: list[ELEM],
        w: list[list[ELEM | None]],  # column ordered alignment
        symbols: set[ELEM]
):
    transition_probabilities = {}
    emission_probabilities = {}
    sequences = [v, w]
    axes = [[None] + av for av in sequences]
    axes_len = [range(len(axis)) for axis in axes]
    transition_probabilities['SOURCE'] = {}
    transition_probabilities['SOURCE'][0, 0, 'EMIT'] = 0.5
    transition_probabilities['SOURCE'][0, 0, 'SILENT'] = 0.5
    for hmm_from_v_idx, hmm_from_w_idx in product(*axes_len):
        hmm_from_n_id = hmm_from_v_idx, hmm_from_w_idx
        transition_probabilities[hmm_from_n_id] = {}
        hmm_to_n_id = hmm_from_v_idx, hmm_from_w_idx + 1
        if hmm_to_n_id in transition_probabilities:  # skip if neighbouring node doesn't exist
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = 0.0
            emission_probabilities[hmm_to_n_id] = {'?'}
        hmm_to_n_id = hmm_from_v_idx + 1, hmm_from_w_idx
        if hmm_to_n_id in transition_probabilities:  # skip if neighbouring node doesn't exist
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = 0.0
            emission_probabilities[hmm_to_n_id] = {}  # no-emission
        hmm_to_n_id = hmm_from_v_idx + 1, hmm_from_w_idx + 1, 'EMIT'
        if hmm_to_n_id in transition_probabilities:  # skip if neighbouring node doesn't exist
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = 0.0
            emission_probabilities[hmm_to_n_id] = {'?'}
    print(f'{transition_probabilities}')


alignment_to_hmm(
    list('n'),
    [['a'], ['n'], ['a']],
    set()
)