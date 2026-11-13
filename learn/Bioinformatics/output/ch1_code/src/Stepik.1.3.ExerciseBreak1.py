import sys

from FindLocationsOfAKnownKmer import find_kmer_locations

#with sys.stdin as f:
with open('/home/user/Downloads/Vibrio_cholerae.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

arr = find_kmer_locations(data, 'CTTGATCAT')

print(f'{" ".join([str(pos) for pos in arr])}')