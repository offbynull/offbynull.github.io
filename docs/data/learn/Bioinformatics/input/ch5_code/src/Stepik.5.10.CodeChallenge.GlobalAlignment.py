from global_alignment.GlobalAlignment_Graph import global_alignment
from scoring.WeightLookup import TableWeightLookup

with open('/home/user/Downloads/dataset_240305_3(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')

s1 = list(lines[0].strip())
s2 = list(lines[1].strip())
weight_lookup = TableWeightLookup.create_from_2d_matrix_file('BLOSUM62.txt', -5)
final_weight, alignment = global_alignment(s1, s2, weight_lookup)

print(f'{int(final_weight)}')
for row in alignment:
    for e in row:
        print(f'{"-" if e is None else e}', end='')
    print('')
