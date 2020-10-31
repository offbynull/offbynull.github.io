import sys

#with sys.stdin as f:
from FindLocationsOfAKnownKmerWithMismatches import find_kmer_locations_with_mismatches
from HammingDistanceBetweenKmers import hamming_distance

with open('/home/user/Downloads/dataset_240221_4(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmer = lines[0]
seq = lines[1]
hamming_dist = int(lines[2])

mismatch = find_kmer_locations_with_mismatches(seq, kmer, hamming_dist)

print(f'{" ".join([str(m) for m in mismatch])}')