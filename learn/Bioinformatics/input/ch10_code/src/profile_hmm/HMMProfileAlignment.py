from sys import stdin

import yaml

from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import to_hmm_graph_PRE_PSEUDOCOUNTS, \
    hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot, to_viterbi_graph, max_product_path_in_viterbi, \
    viterbi_to_dot
from profile_hmm.AlignmentToProfile import Profile
from profile_hmm.HMMSequenceAlignment import create_hmm_chain_from_v_perspective
from profile_hmm.HMMSingleElementAlignment_EmitDelete import ELEM, stringify_probability_keys
from profile_hmm.ProfileToHMMProbabilities import profile_to_emission_probabilities, profile_to_transition_probabilities


# MARKDOWN_STRUCT
def create_profile_hmm_structure(
        v_seq: list[ELEM],
        w_profile: Profile[ELEM],
        t_elem: ELEM
):
    # Create fake w_seq based on profile, just to feed into function for it to create the structure. This won't set any
    # probabilities (what's being returned are collections filled with NaN values).
    w_seq = [v_seq[0] for x in range(w_profile.col_count)]
    transition_probabilities, emission_probabilities = create_hmm_chain_from_v_perspective(v_seq, w_seq, t_elem)
    return transition_probabilities, emission_probabilities
# MARKDOWN_STRUCT


def main_structure():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        sequence = data['sequence']
        alignment = data['alignment']
        for seq in alignment:
            for i, e in enumerate(seq):
                if e == '-':
                    seq[i] = None
        column_removal_threshold = data['column_removal_threshold']
        print(f'Building profile using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        profile = Profile(
            alignment,
            column_removal_threshold
        )
        transition_probabilities, emission_probabilities = create_profile_hmm_structure(
            sequence,
            profile,
            '?'
        )
        transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities, emission_probabilities)
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced (structure only, no probabilities)...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")
















# MARKDOWN_PROFILE
def hmm_profile_alignment(
        v_seq: list[ELEM],
        w_profile: Profile[ELEM],
        t_elem: ELEM,
        symbols: set[ELEM],
        pseudocount: float
):
    # Build graph
    transition_probabilities, emission_probabilities = create_profile_hmm_structure(v_seq, w_profile, t_elem)
    # Generate probabilities from profile
    emission_probabilities_overrides = profile_to_emission_probabilities(w_profile)
    transition_probability_overrides = profile_to_transition_probabilities(w_profile)
    # Apply generated transition probabilities
    for hmm_from_n_id in transition_probabilities:
        for hmm_to_n_id in transition_probabilities[hmm_from_n_id]:
            if hmm_to_n_id[0] == 'T':
                value = 1.0  # 100% chance of going to sink node
            else:
                _, _, row = hmm_from_n_id
                row -= 1
                direction, _, _ = hmm_to_n_id
                value = transition_probability_overrides[row][direction]
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = value
    # Apply generated emission probabilities
    for hmm_to_n_id in emission_probabilities:
        if hmm_to_n_id[0] == 'S':
            ...  # skip source, it's non-emitting
        elif hmm_to_n_id[0] == 'T':
            ...  # skip sink node, should have a single emission set to t_elem, which should already be in place
        elif hmm_to_n_id[0] == 'D':
            ...  # skip D nodes (deletions) as they are silent states (no emissions should happen)
        elif hmm_to_n_id[0] in {'I', 'M'}:
            direction, _, row = hmm_to_n_id
            row -= 1
            emit_probs = {sym: 0.0 for sym in symbols}
            emit_probs.update(emission_probabilities_overrides[row, direction])
            emission_probabilities[hmm_to_n_id] = emit_probs
        else:
            raise ValueError('Unknown node type -- this should never happen')
    # Build and apply pseudocounts
    transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities,
                                                                                  emission_probabilities)
    hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
    hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm,
        pseudocount
    )
    hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm,
        pseudocount
    )
    # Get most probable hidden path (viterbi algorithm)
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
# MARKDOWN_PROFILE


def main_profile():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        sequence = data['sequence']
        alignment = data['alignment']
        for seq in alignment:
            for i, e in enumerate(seq):
                if e == '-':
                    seq[i] = None
        pseudocount = data['pseudocount']
        symbols = set(data['symbols'])
        column_removal_threshold = data['column_removal_threshold']
        print(f'Building profile HMM and testing against sequence using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        symbols.add('?')
        profile = Profile(
            alignment,
            column_removal_threshold
        )
        hmm, viterbi, weight, hidden_path, v_alignment = hmm_profile_alignment(sequence, profile, '?', symbols, pseudocount)
        print(f'The following HMM was produced AFTER applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        print(f'The following Viterbi graph was produced for the HMM and the emitted sequence {sequence} ...')
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
    main_profile()
