from typing import Dict, List, Tuple

from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from Utils import slide_window


# MARKDOWN
# Run this on the counts before generating the profile to avoid the 0 probability problem.
def apply_psuedocounts_to_count_matrix(counts: Dict[str, List[int]], extra_count: int = 1):
    for elem, elem_counts in counts.items():
        for i in range(len(elem_counts)):
            elem_counts[i] += extra_count


# Recall that a profile matrix is a matrix of probabilities. Each row represents a single element (e.g. nucleotide) and
# each column represents the probability distribution for that position.
#
# So for example, imagine the following probability distribution...
#
#     1   2   3   4
# A: 0.2 0.2 0.0 0.0
# C: 0.1 0.6 0.0 0.0
# G: 0.1 0.0 1.0 1.0
# T: 0.7 0.2 0.0 0.0
#
# At position 2, the probability that the element will be C is 0.6 while the probability that it'll be T is 0.2. Note
# how each column sums to 1.
def determine_probability_of_match_using_profile_matrix(profile: Dict[str, List[float]], kmer: str):
    prob = 1.0
    for idx, elem in enumerate(kmer):
        prob = prob * profile[elem][idx]
    return prob


def find_most_probable_kmer_using_profile_matrix(profile: Dict[str, List[float]], dna: str):
    k = len(list(profile.values())[0])

    most_probable: Tuple[str, float] = None  # [kmer, probability]
    for kmer, _ in slide_window(dna, k):
        prob = determine_probability_of_match_using_profile_matrix(profile, kmer)
        if most_probable is None or prob > most_probable[1]:
            most_probable = (kmer, prob)

    return most_probable
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break
        
        kmer = dnas[-1]
        motif_matrix = dnas[:-2]

        counts = motif_matrix_count(motif_matrix)
        profile = motif_matrix_profile(counts)
        prob = determine_probability_of_match_using_profile_matrix(profile, kmer)
        print(f'Motif matrix...\n\n')
        print(f'{"<br>".join(motif_matrix)}\n\n')
        print(f'Probability that {kmer} matches the motif {prob}...\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")