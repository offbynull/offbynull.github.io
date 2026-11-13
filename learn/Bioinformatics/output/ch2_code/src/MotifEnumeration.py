from typing import Set, List

from FindAllDnaKmersWithinHammingDistance import find_all_dna_kmers_within_hamming_distance
from HammingDistanceBetweenKmers import hamming_distance
from Utils import slide_window

# MARKDOWN
# Don't get confused by this method. It enumerates every possible kmer that COULD be the motif. That is, every possible
# kmer that has a matching kmer in each string in dnas[]. "Matching kmer" in this case means matching within some
# hamming distance.
def motif_enumeration(
        dnas: List[str],      # dna strings to search in for motif
        k: int,               # k-mer length
        max_mismatches: int   # max num of mismatches for motif (hamming dist)
) -> Set[str]:
    found_kmers = set()

    kmers_to_check = set()
    for dna in dnas:
        for kmer, _ in slide_window(dna, k):
            neighbouring_kmers = find_all_dna_kmers_within_hamming_distance(kmer, max_mismatches)
            kmers_to_check |= neighbouring_kmers

    for kmer_to_check in kmers_to_check:
        found_count = 0
        for dna in dnas:
            for other_kmer, _ in slide_window(dna, k):
                if hamming_distance(kmer_to_check, other_kmer) <= max_mismatches:
                    found_count += 1
                    break
        if found_count == len(dnas):
            found_kmers.add(kmer_to_check)

    return found_kmers
# MARKDOWN


# EXAMPLE INPUT: (make sure to send EOF signal to begin processing, it may take forever to finish)
#
# 9
# 2
# atgaccgggatactgatAgAAgAAAGGttGGGggcgtacacattagataaacgtatgaagtacgttagactcggcgccgccg
# acccctattttttgagcagatttagtgacctggaaaaaaaatttgagtacaaaacttttccgaatacAAtAAAAcGGcGGGa
# tgagtatccctgggatgacttAAAAtAAtGGaGtGGtgctctcccgatttttgaatatgtaggatcattcgccagggtccga
# gctgagaattggatgcAAAAAAAGGGattGtccacgcaatcgcgaaccaacgcggacccaaaggcaagaccgataaaggaga
# tcccttttgcggtaatgtgccgggaggctggttacgtagggaagccctaacggacttaatAtAAtAAAGGaaGGGcttatag
# gtcaatcatgttcttgtgaatggatttAAcAAtAAGGGctGGgaccgcttggcgcacccaaattcagtgtgggcgagcgcaa
# cggttttggcccttgttagaggcccccgtAtAAAcAAGGaGGGccaattatgagagagctaatctatcgcgtgcgtgttcat
# acttgagttAAAAAAtAGGGaGccctggggcacatacaagaggagtcttccttatcagttaatgctgtatgacactatgta
# ttggcccattggctaaaagcccaacttgacaaatggaagatagaatccttgcatActAAAAAGGaGcGGaccgaaagggaag
# ctggtgagcaacgacagattcttacgtgcattagctcgcttccggggatctaatagcacgaagcttActAAAAAGGaGcGGa

def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        k = int(input())
        max_mismatches = int(input())
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break

        motifs = motif_enumeration(dnas, k, max_mismatches)
        print(f'Found ... {"<br>".join(motifs)}<br>... in ...<br> {"<br>".join(dnas)}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

