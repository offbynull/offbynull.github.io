`{bm-disable-all}`[ch1_code/src/FindClumps.py](ch1_code/src/FindClumps.py) (lines 10 to 26):`{bm-enable-all}`

```python
def find_kmer_clusters(sequence: str, kmer: str, min_occurrence_in_cluster: int, cluster_window_size: int, options: Options = Options()) -> List[int]:
    cluster_locs = []

    locs = find_kmer_locations(sequence, kmer, options)
    start_i = 0
    occurrence_count = 1
    for end_i in range(1, len(locs)):
        if locs[end_i] - locs[start_i] < cluster_window_size:  # within a cluster window?
            occurrence_count += 1
        else:
            if occurrence_count >= min_occurrence_in_cluster:  # did the last cluster meet the min ocurr requirement?
                cluster_locs.append(locs[start_i])
            start_i = end_i
            occurrence_count = 1

    return cluster_locs
```