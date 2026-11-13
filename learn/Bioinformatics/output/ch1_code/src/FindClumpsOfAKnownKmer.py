from __future__ import annotations

from typing import List
from FindLocationsOfAKnownKmer import find_kmer_locations


# MARKDOWN
def find_kmer_clusters(sequence: str, kmer: str, min_occurrence_in_cluster: int, cluster_window_size: int) -> List[int]:
    cluster_locs = []

    locs = find_kmer_locations(sequence, kmer)
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
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        kmer = input()
        min_occurrence_in_cluster = int(input())
        cluster_window_size = int(input())
        idxes = find_kmer_clusters(seq, kmer, min_occurrence_in_cluster, cluster_window_size)
        print(f'Found clusters of {kmer} (at least {min_occurrence_in_cluster} occurrences in window of {cluster_window_size}) in {seq} at index {idxes}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()