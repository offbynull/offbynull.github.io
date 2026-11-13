from typing import List, Tuple

from HammingDistanceBetweenKmers import hamming_distance
from Utils import enumerate_patterns, slide_window


# MARKDOWN
# The name is slightly confusing. What this actually does...
#   For each dna string:
#     Find the k-mer with the min hamming distance between the k-mers that make up the DNA string and pattern
#   Sum up the min hamming distances of the found k-mers (equivalent to the motif matrix score)
def distance_between_pattern_and_strings(pattern: str, dnas: List[str]) -> int:
    min_hds = []

    k = len(pattern)
    for dna in dnas:
        min_hd = None
        for dna_kmer, _ in slide_window(dna, k):
            hd = hamming_distance(pattern, dna_kmer)
            if min_hd is None or hd < min_hd:
                min_hd = hd
        min_hds.append(min_hd)
    return sum(min_hds)


def median_string(k: int, dnas: List[str]):
    last_best: Tuple[str, int] = None  # last found consensus string and its score
    for kmer in enumerate_patterns(k):
        score = distance_between_pattern_and_strings(kmer, dnas)  # find score of best motif matrix where consensus str is kmer
        if last_best is None or score < last_best[1]:
            last_best = kmer, score
    return last_best
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

        kmer, score = median_string(k, dnas)
        print(f'Searching for motif of k={k} in the following...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'Found the consensus string {kmer} with a score of {score}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()