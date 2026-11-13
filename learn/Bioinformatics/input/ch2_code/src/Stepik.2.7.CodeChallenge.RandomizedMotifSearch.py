from RandomizedMotifMatrixSearchWithPsuedocounts import randomized_motif_search_with_psuedocounts
from ScoreMotif import score_motif

with open('/home/user/Downloads/dataset_240243_5(3).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].split()[0])
dnas_count = int(lines[0].split()[1])  # ignore
dnas = lines[1:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

best_motif_matrix = None
for i in range(1000):
    found_motif_matrix = randomized_motif_search_with_psuedocounts(k, dnas)
    if best_motif_matrix is None:
        best_motif_matrix = found_motif_matrix
    elif score_motif(found_motif_matrix) < score_motif(best_motif_matrix):
        best_motif_matrix = found_motif_matrix

for motif in best_motif_matrix:
    print(f'{motif}')
