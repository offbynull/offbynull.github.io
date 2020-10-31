from collections import Counter
from random import randrange, random, uniform
from typing import List, Dict

from FindMostProbableKmerUsingProfileMatrix import determine_probability_of_match_using_profile_matrix, \
    apply_psuedocounts_to_count_matrix
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif
from Utils import slide_window


# MARKDOWN
def gibbs_rand(prob_dist: List[float]) -> int:
    # normalize prob_dist -- just incase sum(prob_dist) != 1.0
    prob_dist_sum = sum(prob_dist)
    prob_dist = [p / prob_dist_sum for p in prob_dist]

    while True:
        selection = randrange(0, len(prob_dist))
        if random() < prob_dist[selection]:
            return selection


def determine_probabilities_of_all_kmers_in_dna(profile_matrix: Dict[str, List[float]], dna: str, k: int) -> List[int]:
    ret = []
    for kmer, _ in slide_window(dna, k):
        prob = determine_probability_of_match_using_profile_matrix(profile_matrix, kmer)
        ret.append(prob)
    return ret


def gibbs_sampler_motif_search_with_psuedocounts(k: int, dnas: List[str], cycles: int) -> List[str]:
    motif_matrix = []
    for dna in dnas:
        start = randrange(len(dna) - k + 1)
        kmer = dna[start:start + k]
        motif_matrix.append(kmer)

    best_motif_matrix = motif_matrix[:]  # create a copy, otherwise you'll be modifying both motif and best_motif

    for j in range(0, cycles):
        i = randrange(len(dnas))  # pick a dna
        del motif_matrix[i]  # remove the kmer for that dna from the motif str

        counts = motif_matrix_count(motif_matrix)
        apply_psuedocounts_to_count_matrix(counts)
        profile = motif_matrix_profile(counts)

        new_motif_kmer_probs = determine_probabilities_of_all_kmers_in_dna(profile, dnas[i], k)
        new_motif_kmer_idx = gibbs_rand(new_motif_kmer_probs)
        new_motif_kmer = dnas[i][new_motif_kmer_idx:new_motif_kmer_idx+k]
        motif_matrix.insert(i, new_motif_kmer)

        if score_motif(motif_matrix) < score_motif(best_motif_matrix):
            best_motif_matrix = motif_matrix[:]  # create a copy, otherwise you'll be modifying both motif and best_motif

    return best_motif_matrix
# MARKDOWN


# EXAMPLE INPUT: (make sure to send EOF signal to begin processing, it may take forever to finish)
#
# 1000
# 3
# AAATTGACGCAT
# GACGACCACGTT
# CGTCAGCGCCTG
# GCTGAGCACCGG
# AGTTCGGGACAG

def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        iterations = int(input())
        k = int(input())
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break

        print(f'Searching for motif of k={k} in the following...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'Running {iterations} iterations...\n\n')

        best_motif_matrix = gibbs_sampler_motif_search_with_psuedocounts(k, dnas, iterations)

        print(f'Best found the motif matrix...\n\n')
        print(f'{"<br>".join(best_motif_matrix)}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")