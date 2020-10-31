import sys

from FindASequencesKmerClusters import find_clustered_kmers
from ReverseComplementADnaKmer import reverse_complement

#with sys.stdin as f:
with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]
k = int(lines[1].split(' ')[0])
cluster_window_size = int(lines[1].split(' ')[1])
min_occurrence_in_cluster = int(lines[1].split(' ')[2])

idxes = find_clustered_kmers(seq, k, min_occurrence_in_cluster, cluster_window_size)

print(f'{" ".join(idxes)}')