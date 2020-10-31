from collections import Counter
from typing import List, Dict


# For each column in a motif matrix, count up how many times each nucleotide appears.
# MARKDOWN
def motif_matrix_count(motif_matrix: List[str], elements='ACGT') -> Dict[str, List[int]]:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    ret = {}
    for ch in elements:
        ret[ch] = [0] * cols
    
    for c in range(0, cols):
        for r in range(0, rows):
            item = motif_matrix[r][c]
            ret[item][c] += 1
            
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
        print(f'Counting nucleotides at each column of the motif matrix...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'Result...\n\n')
        print(f'{"<br>".join([str(i) for i in counts.items()])}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
