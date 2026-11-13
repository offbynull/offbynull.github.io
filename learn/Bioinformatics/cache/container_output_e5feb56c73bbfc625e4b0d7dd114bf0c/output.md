`{bm-disable-all}`[ch2_code/src/ExhaustiveMotifMatrixSearch.py](ch2_code/src/ExhaustiveMotifMatrixSearch.py) (lines 9 to 41):`{bm-enable-all}`

```python
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
```