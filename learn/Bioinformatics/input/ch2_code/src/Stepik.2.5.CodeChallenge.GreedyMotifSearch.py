from GreedyMotifMatrixSearch import greedy_motif_search

with open('/home/user/Downloads/dataset_240241_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].split()[0])
dnas_count = int(lines[0].split()[1])  # ignore
dnas = lines[1:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

found_motif_matrix = greedy_motif_search(k, dnas)
for motif in found_motif_matrix:
    print(f'{motif}')
