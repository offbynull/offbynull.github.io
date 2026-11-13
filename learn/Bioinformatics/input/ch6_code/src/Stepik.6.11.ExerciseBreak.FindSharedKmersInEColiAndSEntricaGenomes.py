from helpers.DnaUtils import dna_reverse_complement
from helpers.Utils import slide_window

# This is doing the exact same thing as the CodeChallenge but on much larger sequences. I didn't include the files
# in the project because they'd take too much space in the git repo.
with open('/home/user/Downloads/E_coli.txt', 'r') as ef, open('/home/user/Downloads/Salmonella_enterica.txt', 'r') as sf:
    dna1 = ef.read()
    dna2 = sf.read()
k = 30

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

print(f'{found}')
print(f'{len(found)}')