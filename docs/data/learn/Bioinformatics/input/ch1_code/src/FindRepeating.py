from __future__ import annotations

from collections import Counter
from typing import Set

from FindAllDnaKmersWithinHammingDistance import find_all_dna_kmers_within_hamming_distance
from FindLocations import Options
from ReverseComplementADnaKmer import reverse_complement


# MARKDOWN
from Utils import slide_window


def count_kmers(data: str, k: int, options: Options = Options()) -> Counter[str]:
    counter = Counter()
    for kmer, i in slide_window(data, k):
        neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer, options.hamming_distance)
        for neighbouring_kmer in neighbourhood:
            counter[neighbouring_kmer] += 1

        if options.reverse_complement:
            kmer_rc = reverse_complement(kmer)
            neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer_rc, options.hamming_distance)
            for neighbouring_kmer in neighbourhood:
                counter[neighbouring_kmer] += 1

    return counter


def top_repeating_kmers(data: str, k: int, options: Options = Options()) -> Set[str]:
    counts = count_kmers(data, k, options)

    _, top_count = counts.most_common(1)[0]

    top_kmers = set()
    for kmer, count in counts.items():
        if count == top_count:
            top_kmers.add((kmer, count))
    return top_kmers
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        k = int(input())
        hamming_distance = int(input())
        reverse_complement = bool(input())

        top_kmers = top_repeating_kmers(seq, k, Options(hamming_distance, reverse_complement))

        print(f'Top {k}-mer frequencies for {seq}:')
        [print(f' * {key} = {value} occurrences') for key, value in top_kmers]
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()