from collections import Counter
from math import log
from typing import List

from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile


# MARKDOWN
# According to the book, method of scoring a motif matrix as defined in ScoreMotif.py isn't the method used in the
# real-world. The method used in the real-world is this method, where...
# 1. each column has its probability distribution calculated (prob of A vs prob C vs prob of T vs prob of G)
# 2. the entropy of each of those prob dist are calculated
# 3. those entropies are summed up to get the ENTROPY OF THE MOTIF MATRIX
def calculate_entropy(values: List[float]) -> float:
    ret = 0.0
    for value in values:
        ret += value * (log(value, 2.0) if value > 0.0 else 0.0)
    ret = -ret
    return ret

def score_motify_entropy(motif_matrix: List[str]) -> float:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    # count up each column
    counts = motif_matrix_count(motif_matrix)
    profile = motif_matrix_profile(counts)

    # prob dist to entropy
    entropy_per_col = []
    for c in range(cols):
        entropy = calculate_entropy([profile['A'][c], profile['C'][c], profile['G'][c], profile['T'][c]])
        entropy_per_col.append(entropy)

    # sum up entropies to get entropy of motif
    return sum(entropy_per_col)
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

        score = score_motify_entropy(dnas)
        print(f'Scoring...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'{score}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()