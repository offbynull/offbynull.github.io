from collections import Counter

from FindLocationsOfAKnownKmerWithMismatches import find_kmer_locations_with_mismatches

seq = 'AACAAGCTGATAAACATTTAAAGAG'
kmer = 'AAAAA'
min_hamming_dist = 2

locs = find_kmer_locations_with_mismatches(seq, kmer, min_hamming_dist)

print(f'{len(locs)}')