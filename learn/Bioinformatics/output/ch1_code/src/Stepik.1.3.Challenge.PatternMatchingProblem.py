import sys

from FindLocationsOfAKnownKmer import find_kmer_locations

#with sys.stdin as f:
with open('/home/user/Downloads/dataset_240215_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmer = lines[0]
seq = lines[1]

arr = find_kmer_locations(seq, kmer)

print(f'{" ".join([str(pos) for pos in arr])}')