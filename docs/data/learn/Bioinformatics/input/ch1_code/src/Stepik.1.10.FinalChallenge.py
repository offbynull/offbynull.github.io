import hashlib
import textwrap

import matplotlib.pyplot as plt

from CountASequencesKmersWithMismatchesAndReverseComplement import \
    kmer_frequency_with_mismatches_and_reverse_complements
from GCSkew import gc_skew

with open('/home/user/Downloads/Salmonella_enterica.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

skew = gc_skew(data)

min_value = min(skew)
min_index = skew.index(min_value)

print(f'{min_index}')

for i in range(min_index - 250, min_index + 250):
    counts = kmer_frequency_with_mismatches_and_reverse_complements(data[i - 250:i + 250], 9, 1)
    _, top_count = counts.most_common(1)[0]
    top_kmers = []
    for kmer, count in counts.items():
        if count == top_count:
            top_kmers.append((kmer, count))

    print(f'{top_kmers}')