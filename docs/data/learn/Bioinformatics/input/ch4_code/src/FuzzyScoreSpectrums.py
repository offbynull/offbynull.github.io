from collections import Counter
from typing import List, Union, TypeVar

from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide


# Count the number of intersections (an item must be in BOTH lists to be included). For example...
# [0, 99, 113, 128] vs [0, 128, 227] has a score of 2 (intersection is [0, 128])
#
# It's assumed that both spectra are sorted smallest to largest.
def score_spectrums(s1: List[int], s2: List[int], mass_tolerance: int = 0) -> int:
    idx_s1 = 0
    idx_s2 = 0
    score = 0
    while idx_s1 < len(s1) and idx_s2 < len(s2):
        s1_mass = s1[idx_s1]
        s2_mass = s2[idx_s2]
        s1_mass_lower = s1_mass - mass_tolerance
        s1_mass_upper = s1_mass + mass_tolerance
        s2_mass_lower = s2_mass - mass_tolerance
        s2_mass_upper = s2_mass + mass_tolerance
        if s2_mass_lower > s1_mass_upper:
            idx_s1 += 1
        elif s1_mass_lower > s2_mass_upper:
            idx_s2 += 1
        else:
            idx_s1 += 1
            idx_s2 += 1
            score += 1
    return score


T = TypeVar('T')


# Score a set of peptides against a reference spectrum and return the top n (including ties at the end, so it may be end
# up being more than n).
def top_n_peptides_including_last_place_ties(
        peptides: List[Union[str, List[T]]],
        reference_spectrum: List[int],
        n: int,
        mass_table=None,
        mass_tolerance: int = 0
) -> List[Union[str, List[T]]]:
    if len(peptides) == 0:
        return peptides

    spectrums = [theoretical_spectrum_of_linear_peptide(p, mass_table) for p in peptides]
    scores = [score_spectrums(s, reference_spectrum, mass_tolerance=mass_tolerance) for s in spectrums]
    sorted_peptide_scores = list(sorted(zip(peptides, scores), key=lambda x: x[1], reverse=True))  # big to small

    # Return first n elements from sorted_peptide_scores, but since we're including ending ties we need to check if the
    # element at n repeats. If it does, include the repeats (the result wil be larger than n).
    for j in range(n + 1, len(sorted_peptide_scores)):
        if sorted_peptide_scores[n][1] > sorted_peptide_scores[j][1]:
            return [p for p, _ in sorted_peptide_scores[:j-1]]
    return [p for p, _ in sorted_peptide_scores]


if __name__ == '__main__':
    print(f'{score_spectrums([0, 98, 113, 128], [0, 97, 129, 227], mass_tolerance=1)}')
    # leaderboard = ['LAST', 'ALST', 'TLLT', 'TQAS']
    # leaderboard = top_n_peptides_including_last_place_ties(
    #     leaderboard,
    #     [0, 71, 87, 101, 113, 158, 184, 188, 259, 271, 372],
    #     2,
    #     mass_tolerance=900)
    # print(f'{leaderboard}')