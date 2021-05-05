`{bm-disable-all}`[ch1_code/src/FindRepeatingInWindow.py](ch1_code/src/FindRepeatingInWindow.py) (lines 20 to 67):`{bm-enable-all}`

```python
def scan_for_repeating_kmers_in_clusters(sequence: str, k: int, min_occurrence_in_cluster: int, cluster_window_size: int, options: Options = Options()) -> Set[KmerCluster]:
    def neighborhood(kmer: str) -> Set[str]:
        neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer, options.hamming_distance)
        if options.reverse_complement:
            kmer_rc = reverse_complement(kmer)
            neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer_rc, options.hamming_distance)
        return neighbourhood

    kmer_counter = {}

    def add_kmer(kmer: str, loc: int) -> None:
        if kmer not in kmer_counter:
            kmer_counter[kmer] = set()
        kmer_counter[kmer].add(window_idx + kmer_idx)

    def remove_kmer(kmer: str, loc: int) -> None:
        kmer_counter[kmer].remove(window_idx - 1)
        if len(kmer_counter[kmer]) == 0:
            del kmer_counter[kmer]

    clustered_kmers = set()

    old_first_kmer = None
    for window, window_idx in slide_window(sequence, cluster_window_size):
        first_kmer = window[0:k]
        last_kmer = window[-k:]

        # If first iteration, add all kmers
        if window_idx == 0:
            for kmer, kmer_idx in slide_window(window, k):
                for alt_kmer in neighborhood(kmer):
                    add_kmer(alt_kmer, window_idx + kmer_idx)
        else:
            # Add kmer that was walked in to
            for new_last_kmer in neighborhood(last_kmer):
                add_kmer(new_last_kmer, window_idx + cluster_window_size - k)
            # Remove kmer that was walked out of
            if old_first_kmer is not None:
                for alt_kmer in neighborhood(old_first_kmer):
                    remove_kmer(alt_kmer, window_idx - 1)

        old_first_kmer = first_kmer

        # Find clusters within window -- tuple is k-mer, start_idx, occurrence_count
        [clustered_kmers.add(KmerCluster(k, min(v), len(v))) for k, v in kmer_counter.items() if len(v) >= min_occurrence_in_cluster]

    return clustered_kmers
```