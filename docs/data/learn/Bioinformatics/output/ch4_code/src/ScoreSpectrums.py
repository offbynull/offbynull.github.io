from typing import List
from LeaderboardCyclopeptideSequencing import top_n_peptides_including_last_place_ties


# Count the number of intersections (an item must be in BOTH lists to be included). For example...
# [0, 99, 113, 128] vs [0, 128, 227] has a score of 2 (intersection is [0, 128])
#
# It's assumed that both spectra are sorted smallest to largest.
def score_spectrums(s1: List[int], s2: List[int]) -> int:
    idx_s1 = 0
    idx_s2 = 0
    score = 0
    while idx_s1 < len(s1) and idx_s2 < len(s2):
        s1_mass = s1[idx_s1]
        s2_mass = s2[idx_s2]
        if s1_mass < s2_mass:
            idx_s1 += 1
        elif s1_mass > s2_mass:
            idx_s2 += 1
        else:
            idx_s1 += 1
            idx_s2 += 1
            score += 1
    return score


if __name__ == '__main__':
    leaderboard = ['LAST', 'ALST', 'TLLT', 'TQAS']
    leaderboard = top_n_peptides_including_last_place_ties(
        leaderboard,
        [0, 71, 87, 101, 113, 158, 184, 188, 259, 271, 372],
        2)
    print(f'{leaderboard}')