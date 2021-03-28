from helpers.DnaUtils import dna_reverse_complement
from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240326_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = [l.strip() for l in data.strip().split('\n')]
k = int(lines[0])
dna1 = lines[1]
dna2 = lines[2]

def find_shared_kmers(dna1, dna2):
    dna1_found_idxes = {}
    for kmer, idx in slide_window(dna1, k):
        dna1_found_idxes.setdefault(kmer, []).append(idx)

    found = []
    for kmer, idx in slide_window(dna2, k):
        kmer_rc = dna_reverse_complement(kmer)
        other_idxes = []
        if kmer in dna1_found_idxes:
            other_idxes += dna1_found_idxes[kmer]
        if kmer_rc in dna1_found_idxes:
            other_idxes += dna1_found_idxes[kmer_rc]
        for i in other_idxes:
            found += [(i, idx)]

    found.sort()
    return found


for found in find_shared_kmers(dna1, dna2):
    print(f'{found}')
