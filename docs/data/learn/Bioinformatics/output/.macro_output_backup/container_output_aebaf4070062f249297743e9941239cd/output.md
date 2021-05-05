`{bm-disable-all}`[ch2_code/src/RandomizedMotifMatrixSearchWithPsuedocounts.py](ch2_code/src/RandomizedMotifMatrixSearchWithPsuedocounts.py) (lines 13 to 32):`{bm-enable-all}`

```python
def randomized_motif_search_with_psuedocounts(k: int, dnas: List[str]) -> List[str]:
        motif_matrix = []
        for dna in dnas:
            start = randrange(len(dna) - k + 1)
            kmer = dna[start:start + k]
            motif_matrix.append(kmer)

        best_motif_matrix = motif_matrix

        while True:
            counts = motif_matrix_count(motif_matrix)
            apply_psuedocounts_to_count_matrix(counts)
            profile = motif_matrix_profile(counts)

            motif_matrix = [find_most_probable_kmer_using_profile_matrix(profile, dna)[0] for dna in dnas]
            if score_motif(motif_matrix) < score_motif(best_motif_matrix):
                best_motif_matrix = motif_matrix
            else:
                return best_motif_matrix
```