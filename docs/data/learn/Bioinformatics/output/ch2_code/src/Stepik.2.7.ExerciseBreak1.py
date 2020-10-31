from random import randrange

from FindMostProbableKmerUsingProfileMatrix import find_most_probable_kmer_using_profile_matrix
from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile
from ScoreMotif import score_motif

dnas = ['GGCGTTCAGGCA', 'AAGAATCAGTCA', 'CAAGGAGTTCGC', 'CACGTCAATCAC', 'CAATAATATTCG']
k = 3

motifs = []
for dna in dnas:
    start = randrange(len(dna) - k)
    motif = dna[start:start+k]
    motifs.append(motif)

best_motifs = motifs

while True:
    counts_matrix = motif_matrix_count(motifs)
    for elem, counts in counts_matrix.items():  # add in pseudocounts
        counts_matrix[elem] = [c + 1 for c in counts]
    profile_matrix = motif_matrix_profile(counts_matrix)

    motifs = [find_most_probable_kmer_using_profile_matrix(profile_matrix, dna)[0] for dna in dnas]
    if score_motif(motifs) < score_motif(best_motifs):
        best_motifs = motifs
    else:
        break

[print(f'{m}') for m in best_motifs]