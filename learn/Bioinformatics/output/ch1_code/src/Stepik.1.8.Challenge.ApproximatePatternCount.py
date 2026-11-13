from FindLocationsOfAKnownKmer import find_kmer_locations
from FindLocationsOfAKnownKmerWithMismatches import find_kmer_locations_with_mismatches

with open('/home/user/Downloads/dataset_240221_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmer = lines[0]
seq = lines[1]
min_hamming_dist = int(lines[2])

arr = find_kmer_locations_with_mismatches(seq, kmer, min_hamming_dist)

print(f'{len(arr)}')