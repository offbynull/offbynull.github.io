import hashlib
import textwrap

import matplotlib.pyplot as plt

from CountASequencesKmersWithMismatchesAndReverseComplement import \
    kmer_frequency_with_mismatches_and_reverse_complements
from FindAllDnaKmersWithinHammingDistance import find_all_dna_kmers_within_hamming_distance
from GCSkew import gc_skew

with open('/home/user/Downloads/dataset_240229_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmer = lines[0]
hamming_dist = int(lines[1])

kmer_variations = find_all_dna_kmers_within_hamming_distance(kmer, hamming_dist)
print(f'{" ".join(kmer_variations)}')