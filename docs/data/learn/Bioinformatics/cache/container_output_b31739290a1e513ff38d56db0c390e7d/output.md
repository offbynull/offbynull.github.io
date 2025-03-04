`{bm-disable-all}`[ch2_code/src/HybridAlphabetMatrix.py](ch2_code/src/HybridAlphabetMatrix.py) (lines 5 to 26):`{bm-enable-all}`

```python
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
```