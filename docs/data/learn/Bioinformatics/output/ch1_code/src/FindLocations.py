from __future__ import annotations

from typing import List, NamedTuple

from FindAllDnaKmersWithinHammingDistance import find_all_dna_kmers_within_hamming_distance
from ReverseComplementADnaKmer import reverse_complement
from Utils import slide_window


# MARKDOWN
class Options(NamedTuple):
    hamming_distance: int = 0
    reverse_complement: bool = False


def find_kmer_locations(sequence: str, kmer: str, options: Options = Options()) -> List[int]:
    # Construct test kmers
    test_kmers = set()
    test_kmers.add(kmer)
    [test_kmers.add(alt_kmer) for alt_kmer in find_all_dna_kmers_within_hamming_distance(kmer, options.hamming_distance)]
    if options.reverse_complement:
        rc_kmer = reverse_complement(kmer)
        [test_kmers.add(alt_rc_kmer) for alt_rc_kmer in find_all_dna_kmers_within_hamming_distance(rc_kmer, options.hamming_distance)]

    # Slide over the sequence's kmers and check for matches against test kmers
    k = len(kmer)
    idxes = []
    for seq_kmer, i in slide_window(sequence, k):
        if seq_kmer in test_kmers:
            idxes.append(i)
    return idxes
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        kmer = input()
        hamming_distance = int(input())
        reverse_complement = bool(input())
        idxes = find_kmer_locations(seq, kmer, Options(hamming_distance, reverse_complement))
        print(f'Found {kmer} in {seq} at index {idxes}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()