from typing import Set, List

from FindAllDnaKmersWithinHammingDistance import find_all_dna_kmers_within_hamming_distance
from ScoreMotif import score_motif
from Utils import slide_window


# MARKDOWN
def enumerate_hamming_distance_neighbourhood_for_all_kmer(
        dna: str,             # dna strings to search in for motif
        k: int,               # k-mer length
        max_mismatches: int   # max num of mismatches for motif (hamming dist)
) -> Set[str]:
    kmers_to_check = set()
    for kmer, _ in slide_window(dna, k):
        neighbouring_kmers = find_all_dna_kmers_within_hamming_distance(kmer, max_mismatches)
        kmers_to_check |= neighbouring_kmers

    return kmers_to_check


def exhaustive_motif_search(dnas: List[str], k: int, max_mismatches: int):
    kmers_for_dnas = [enumerate_hamming_distance_neighbourhood_for_all_kmer(dna, k, max_mismatches) for dna in dnas]

    def build_next_matrix(out_matrix: List[str]):
        idx = len(out_matrix)
        if len(kmers_for_dnas) == idx:
            yield out_matrix[:]
        else:
            for kmer in kmers_for_dnas[idx]:
                out_matrix.append(kmer)
                yield from build_next_matrix(out_matrix)
                out_matrix.pop()

    best_motif_matrix = None
    for next_motif_matrix in build_next_matrix([]):
        if best_motif_matrix is None or score_motif(next_motif_matrix) < score_motif(best_motif_matrix):
            best_motif_matrix = next_motif_matrix

    return best_motif_matrix
# MARKDOWN


# EXAMPLE INPUT: (make sure to send EOF signal to begin processing, it may take forever to finish)
#
# 5
# 1
# ataaagggata
# acagaaatgat
# tgaaataacct

def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        k = int(input())
        max_mismatches = int(input())
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break

        motifs = exhaustive_motif_search(dnas, k, max_mismatches)
        print(f'Searching for motif of k={k} and a max of {max_mismatches} mismatches in the following...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'Found the motif matrix...\n\n')
        print(f'{"<br>".join(motifs)}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

