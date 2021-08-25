`{bm-disable-all}`[ch2_code/src/GreedyMotifMatrixSearchWithPsuedocounts.py](ch2_code/src/GreedyMotifMatrixSearchWithPsuedocounts.py) (lines 12 to 33):`{bm-enable-all}`

```python
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
```