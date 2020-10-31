import sys

from FindASequencesKmerClusters import find_clustered_kmers
from ReverseComplementADnaKmer import reverse_complement

#with sys.stdin as f:
with open('/home/user/Downloads/E_coli.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

seq = data.upper().replace('\n', '')
k = 9
cluster_window_size = 500
min_occurrence_in_cluster = 3

idxes = find_clustered_kmers(seq, k, min_occurrence_in_cluster, cluster_window_size)

print(f'{len(idxes)}')