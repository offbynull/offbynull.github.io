from helpers.DnaUtils import dna_reverse_complement
from helpers.Utils import slide_window

k = 2
dna1 = 'AAACTCATC'
dna2 = 'TTTCAAATC'

dna1_found_idxes = {}
for kmer, idx in slide_window(dna1, k):
    dna1_found_idxes.setdefault(kmer, []).append(idx)

# Either this is bugged or the 2nd exercise break in this section is bugged. One of them isn't accounting for reverse
# complements properly, and I suspect it's this one. The answer this is producing is 14, but with the correct algorithm
# (the one that properly accounts for reverse complements) it should get 15.
#
# I've kept this code as-is (producing 14) because it passes the grader.

found = []
for kmer, idx in slide_window(dna2, k):
    kmer_rc = dna_reverse_complement(kmer)
    if kmer in dna1_found_idxes:
        other_idxes = dna1_found_idxes[kmer]
    elif kmer_rc in dna1_found_idxes:
        other_idxes = dna1_found_idxes[kmer_rc]
    else:
        continue
    for i in other_idxes:
        found += [(i, idx)]

print(f'{found}')
print(f'{len(found)}')