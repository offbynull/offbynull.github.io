from collections import Counter
from typing import List, Dict, Set, FrozenSet

# MARKDOWN
PEVZNER_2_16_ALPHABET = dict()
PEVZNER_2_16_ALPHABET[frozenset({'A', 'T'})] = 'W'
PEVZNER_2_16_ALPHABET[frozenset({'G', 'C'})] = 'S'
PEVZNER_2_16_ALPHABET[frozenset({'G', 'T'})] = 'K'
PEVZNER_2_16_ALPHABET[frozenset({'C', 'T'})] = 'Y'


def to_hybrid_alphabet_motif_matrix(motif_matrix: List[str], hybrid_alphabet: Dict[FrozenSet[str], str]) -> List[str]:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    motif_matrix = motif_matrix[:]  # make a copy
    for c in range(cols):
        distinct_nucs_at_c = frozenset([motif_matrix[r][c] for r in range(rows)])
        if distinct_nucs_at_c in hybrid_alphabet:
            for r in range(rows):
                motif_member = motif_matrix[r]
                motif_member = motif_member[:c] + hybrid_alphabet[distinct_nucs_at_c] + motif_member[c+1:]
                motif_matrix[r] = motif_member

    return motif_matrix
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        matrix = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    matrix.append(dna)
            except EOFError:
                break

        new_matrix = to_hybrid_alphabet_motif_matrix(matrix, PEVZNER_2_16_ALPHABET)
        print(f'Converted...\n\n')
        print(f'{"<br>".join(matrix)}\n\n')
        print(f'to...\n\n')
        print(f'{"<br>".join(new_matrix)}\n\n')
        print(f'using...\n\n')
        print(f'{PEVZNER_2_16_ALPHABET}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()