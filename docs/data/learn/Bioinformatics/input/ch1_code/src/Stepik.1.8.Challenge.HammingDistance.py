import sys

#with sys.stdin as f:
from HammingDistanceBetweenKmers import hamming_distance

with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmer1 = lines[0]
kmer2 = lines[1]

mismatch = hamming_distance(kmer1, kmer2)

print(f'{mismatch}')