from collections import Counter
from typing import List, Dict
from MotifMatrixCount import motif_matrix_count


# For each column in a motif matrix, count up how many times each nucleotide appears.
# MARKDOWN
def motif_matrix_profile(motif_matrix_counts: Dict[str, List[int]]) -> Dict[str, List[float]]:
    ret = {}
    for elem, counts in motif_matrix_counts.items():
        ret[elem] = [0.0] * len(counts)

    cols = len(counts)  # all elems should have the same len, so just grab the last one that was walked over
    for i in range(cols):
        total = 0
        for elem in motif_matrix_counts.keys():
            total += motif_matrix_counts[elem][i]
        for elem in motif_matrix_counts.keys():
            ret[elem][i] = motif_matrix_counts[elem][i] / total

    return ret
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

        counts = motif_matrix_count(dnas)
        profile = motif_matrix_profile(counts)
        print(f'Profiling nucleotides at each column of the motif matrix...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'Result...\n\n')
        print(f'{"<br>".join([str(i) for i in profile.items()])}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")