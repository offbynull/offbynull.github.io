from collections import Counter, defaultdict
from sys import stdin

import yaml

from profile_hmm.AlignmentToProfile import Profile


# MARKDOWN_WALK
from profile_hmm.HMMSingleElementAlignment_EmitDelete import ELEM


def walk_row_of_profile(profile: Profile[ELEM], row: int):
    path = []
    stable_col_cnt = profile.col_count
    r = -1
    c = -1
    for stable_col_idx in range(stable_col_cnt):
        # is anything inserted before the stable column? if yes, indicate an insertion
        if profile.insertion_before(stable_col_idx).is_set(row):
            elems = profile.insertion_before(stable_col_idx).values[row]
            path.append(((r, c), (r, c+1), 'I', elems[:]))  # didn't move to next column (stays at c-1)
            c += 1
        # id anything at the stable column? if yes, indicate a match / no, indicate a deletion
        if profile.match(stable_col_idx).is_set(row):
            elem = profile.match(stable_col_idx).values[row]
            path.append(((r, c), (r+1, c+1), 'M', [elem]))  # did move to next column via a match (from c-1 to c)
            r += 1
            c += 1
        else:
            path.append(((r, c), (r+1, c), 'D', []))  # did move to next column via a delete (from c-1 to c)
            r += 1
    if profile.insertion_after(stable_col_cnt-1).is_set(row):
        elems = profile.insertion_after(stable_col_cnt-1).values[row]
        path.append(((r, c), (r, c+1), 'I', elems[:]))
        c += 1
    return path
# MARKDOWN_WALK


def main_walk():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        alignment = data['alignment']
        for seq in alignment:
            for i, e in enumerate(seq):
                if e == '-':
                    seq[i] = None
        column_removal_threshold = data['column_removal_threshold']
        print(f'Building profile and walking profile sequences using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        profile = Profile(
            alignment,
            column_removal_threshold
        )
        print(f'For each sequence in the profile, this is how that sequence would be walked ...')
        print()
        for row in range(profile.row_count):
            walk_sequence = walk_row_of_profile(profile, row)
            print(f' * Sequence in row {row}:')
            for from_n, to_n, type, emissions in walk_sequence:
                print(f'   * Direction {type} (from {from_n} to {to_n})')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_EMISSIONS
def profile_to_emission_probabilities(profile: Profile[ELEM]):
    stable_row_cnt = profile.row_count
    # Count edges by groups
    counts = defaultdict(lambda: Counter())
    for profile_row in range(stable_row_cnt):
        walk = walk_row_of_profile(profile, profile_row)
        for _, (to_r, _), type, elems in walk:
            for elem in elems:
                if elem is not None:
                    counts[to_r, type][elem] += 1
    # Sum up counts for each column and divide to get probabilities
    percs = defaultdict(lambda: {})
    for (from_r, type), symbol_counts in counts.items():
        total = sum(symbol_counts.values())
        for symbol, cnt in symbol_counts.items():
            percs[from_r, type][symbol] = cnt / total
    return percs
# MARKDOWN_EMISSIONS


def main_emissions():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        alignment = data['alignment']
        for seq in alignment:
            for i, e in enumerate(seq):
                if e == '-':
                    seq[i] = None
        column_removal_threshold = data['column_removal_threshold']
        print(f'Building profile and determining emission probabilities using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        profile = Profile(
            alignment,
            column_removal_threshold
        )
        emission_probs = profile_to_emission_probabilities(profile)
        print(f'At each row of the profile, the following emissions are possible ...')
        print()
        for (to_r, type), symbol_percs in emission_probs.items():
            print(f' * Arriving at {to_r} from the {type} direction:')
            for sym, perc in symbol_percs.items():
                print(f'  * {sym}={perc}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







# MARKDOWN_TRANSITIONS
def profile_to_transition_probabilities(profile: Profile[ELEM]):
    stable_row_cnt = profile.row_count
    # Count edges by groups
    counts = defaultdict(lambda: Counter())
    for profile_row in range(stable_row_cnt):
        walk = walk_row_of_profile(profile, profile_row)
        for (from_r, _), _, type, _ in walk:
            counts[from_r][type] += 1
    # Sum up counts for each column and divide to get probabilities
    percs = {}
    for from_r, from_counts in counts.items():
        percs[from_r] = {'I': 0.0, 'M': 0.0, 'D': 0.0}
        total = sum(from_counts.values())
        for k, v in from_counts.items():
            percs[from_r][k] = v / total
    return percs
# MARKDOWN_TRANSITIONS


def main_transitions():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        alignment = data['alignment']
        for seq in alignment:
            for i, e in enumerate(seq):
                if e == '-':
                    seq[i] = None
        column_removal_threshold = data['column_removal_threshold']
        print(f'Building profile and determining transition probabilities using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        profile = Profile(
            alignment,
            column_removal_threshold
        )
        transitions_probs = profile_to_transition_probabilities(profile)
        print(f'At each row of the profile, the following transitions are possible ...')
        print()
        for from_r, trans_percs in transitions_probs.items():
            print(f' * Traveling from {from_r} going in the direction:')
            for dir, perc in trans_percs.items():
                print(f'  * {dir}={perc}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







if __name__ == '__main__':
    main_emissions()