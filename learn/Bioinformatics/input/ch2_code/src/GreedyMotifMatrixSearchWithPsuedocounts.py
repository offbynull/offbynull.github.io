from typing import List, Dict

from FindMostProbableKmerUsingProfileMatrix import find_most_probable_kmer_using_profile_matrix, \
    apply_psuedocounts_to_count_matrix
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif
from Utils import slide_window


# MARKDOWN
def greedy_motif_search_with_psuedocounts(k: int, dnas: List[str]):
    best_motif_matrix = [dna[0:k] for dna in dnas]

    for motif, _ in slide_window(dnas[0], k):
        motif_matrix = [motif]
        counts = motif_matrix_count(motif_matrix)
        apply_psuedocounts_to_count_matrix(counts)
        profile = motif_matrix_profile(counts)

        for dna in dnas[1:]:
            next_motif, _ = find_most_probable_kmer_using_profile_matrix(profile, dna)
            # push in closest kmer as a motif member and recompute profile for the next iteration
            motif_matrix.append(next_motif)
            counts = motif_matrix_count(motif_matrix)
            apply_psuedocounts_to_count_matrix(counts)
            profile = motif_matrix_profile(counts)

        if score_motif(motif_matrix) < score_motif(best_motif_matrix):
            best_motif_matrix = motif_matrix

    return best_motif_matrix
# MARKDOWN


# EXAMPLE INPUT: (make sure to send EOF signal to begin processing, it may take forever to finish)
#
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
        k = int(input())
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break

        found_motif_matrix = greedy_motif_search_with_psuedocounts(k, dnas)
        print(f'Searching for motif of k={k} in the following...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'Found the motif matrix...\n\n')
        print(f'{"<br>".join(found_motif_matrix)}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()