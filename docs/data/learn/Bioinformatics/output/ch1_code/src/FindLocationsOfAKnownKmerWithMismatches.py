from __future__ import annotations

from typing import List


# MARKDOWN
from HammingDistanceBetweenKmers import hamming_distance


def find_kmer_locations_with_mismatches(sequence: str, kmer: str, min_hamming_dist: int) -> List[int]:
    k = len(kmer)
    idxes = []
    for i in range(0, len(sequence) - k + 1):
        if hamming_distance(sequence[i:i + k], kmer) <= min_hamming_dist:
            idxes.append(i)
    return idxes
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        kmer = input()
        min_hamming_dist = int(input())
        idxes = find_kmer_locations_with_mismatches(seq, kmer, min_hamming_dist)
        print(f'Found {kmer} (approximately within hamming distance of {min_hamming_dist}) in {seq} at index {idxes}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()