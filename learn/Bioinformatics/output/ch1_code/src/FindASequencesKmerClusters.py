from __future__ import annotations

from typing import Dict, List
from CountASequencesKmers import kmer_frequency


# MARKDOWN
def find_clustered_kmers(sequence: str, k: int, min_occurrence_in_cluster: int, cluster_window_size: int) -> Dict[str, List[int]]:
    # map kmer to indices
    indices_lookup = dict()
    for i in range(0, len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        if kmer not in indices_lookup:
            indices_lookup[kmer] = []
        indices_lookup[kmer].append(i)

    # check to see if any remaining kmers sit within cluster_window_size
    clumped_kmers = dict()
    for (kmer, indices) in indices_lookup.items():
        for i in range(0, len(indices) - min_occurrence_in_cluster + 1):
            if indices[i + min_occurrence_in_cluster - 1] - indices[i] < cluster_window_size - k:
                clumped_kmers[kmer] = indices
                break

    return clumped_kmers
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        k = int(input())
        min_occurrence_in_cluster = int(input())
        cluster_window_size = int(input())
        print(f'Searching {seq} for clusters of {k}-mer where at least {min_occurrence_in_cluster} occurrences exist in window of {cluster_window_size}\n')
        clusters = find_clustered_kmers(seq, k, min_occurrence_in_cluster, cluster_window_size)
        print(f'Found the following clusters:')
        [print(f' * {kmer}: {idxes}') for kmer, idxes in clusters.items()]
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()