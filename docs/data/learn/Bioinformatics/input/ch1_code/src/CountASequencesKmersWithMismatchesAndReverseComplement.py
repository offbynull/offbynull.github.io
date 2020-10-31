from __future__ import annotations

from collections import Counter

from CountASequencesKmersWithMismatches import kmer_frequency_with_mismatches
from FindAllDnaKmersWithinHammingDistance import find_all_dna_kmers_within_hamming_distance
from FindLocationsOfAKnownKmerWithMismatches import find_kmer_locations_with_mismatches
from ReverseComplementADnaKmer import reverse_complement


# MARKDOWN
def kmer_frequency_with_mismatches_and_reverse_complements(data: str, k: int, min_hamming_dist: int) -> Counter[str]:
    counter = Counter()
    for i in range(0, len(data) - k + 1):
        kmer = data[i:i+k]
        neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer, min_hamming_dist)
        for neighbouring_kmer in neighbourhood:
            counter[neighbouring_kmer] += 1
        kmer_rc = reverse_complement(kmer)
        neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer_rc, min_hamming_dist)
        for neighbouring_kmer in neighbourhood:
            counter[neighbouring_kmer] += 1
    return counter
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        k, min_hamming_dist = [int(x) for x in input().split()]

        counts = kmer_frequency_with_mismatches_and_reverse_complements(seq, k, min_hamming_dist)

        _, top_count = counts.most_common(1)[0]

        top_kmers = []
        for kmer, count in counts.items():
            if count == top_count:
                top_kmers.append((kmer, count))

        print(f'Top {k}-mer frequencies for {seq} with reverse complement and mismatches of {min_hamming_dist}:')
        [print(f' * {key} = {value}') for key, value in top_kmers]
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()