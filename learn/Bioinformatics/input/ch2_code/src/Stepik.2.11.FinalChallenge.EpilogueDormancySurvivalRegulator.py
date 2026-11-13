from FindMostProbableKmerUsingProfileMatrix import determine_probability_of_match_using_profile_matrix
from GibbsSamplerMotifMatrixSearchWithPsuedocounts import gibbs_sampler_motif_search_with_psuedocounts
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif
from Utils import slide_window

# Part 1 - Find a motif matrix

with open('/home/user/Downloads/DosR.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dnas = lines[:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

cycles = 200
k = 20

best_motif_matrix = None
for i in range(20):
    found_motif_matrix = gibbs_sampler_motif_search_with_psuedocounts(k, dnas, cycles)
    if best_motif_matrix is None:
        best_motif_matrix = found_motif_matrix
    elif score_motif(found_motif_matrix) < score_motif(best_motif_matrix):
        best_motif_matrix = found_motif_matrix

for motif in best_motif_matrix:
    print(f'{motif}')
print(f'{score_motif(motif)}')

# Part 2 - Find instances of the motif in the genome

# CGGGACTTCAGGCCCTATCG
# CGGGTCAAACGACCCTAGTG
# CGGGACGTAAGTCCCTAACG
# CCGGGCTTCCAACCGTGGCC
# CGTGACCGACGTCCCCAGCC
# GAGGACCTTCGGCCCCACCC
# GGGGACTTCTGTCCCTAGCC
# TGGGACTTTCGGCCCTGTCC
# GGGGACCAACGCCCCTGGGA
# GGGGACCGAAGTCCCCGGGC
# 11
# consensus_kmer = 'CGGGACCTACGTCCCTAGCC'  # this is consensus string for hte matrix it finds

best_motif_matrix_counts = motif_matrix_count(best_motif_matrix)
for elem, counts in best_motif_matrix_counts.items():  # add in pseudocounts
    best_motif_matrix_counts[elem] = [c + 1 for c in counts]
best_motif_matrix_profile = motif_matrix_profile(best_motif_matrix_counts)

with open('/home/user/Downloads/GCF_000195955.2_ASM19595v2_genomic.fna', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = data.split('\n')
lines = [l.strip() for l in lines]  # get rid of whitespace
lines = [l if not l.startswith('>') else '' for l in lines]  # remove comments
dna = ''.join(lines)  # concat into single dna str
for kmer, _ in slide_window(dna, k):
    prob = determine_probability_of_match_using_profile_matrix(best_motif_matrix_profile, kmer)
    if prob >= 0.01:  # 1% or greater
        print(f'{kmer} {prob}')

# Nothing is found...
#
# The strings in DosR.txt aren't matching up to the genome at the link I posted (even though the name of the organism
# matches). I'm guessing it's a different variant of the organism that was studied in the original 2003 paper. Maybe
# this variant uses a different motif or doesn't have it (doesn't have the ability to lie dormant like the organism that
# the original paper studied).

