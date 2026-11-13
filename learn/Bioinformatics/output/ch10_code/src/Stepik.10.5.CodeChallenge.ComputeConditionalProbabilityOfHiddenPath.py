from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240399_10.txt') as f:
    lines = f.read().splitlines(keepends=False)
emitted_symbols = lines[0]
symbols = lines[2].split()
hidden_path = lines[4]
states = lines[6].split()
emission_probs = {}
mat_head = lines[8].split()
for mat_row in lines[9:]:
    mat_row = mat_row.split()
    state = mat_row[0]
    for i, symbol in enumerate(mat_head):
        emission_probs[state, symbol] = float(mat_row[i + 1])

prob = 1.0
for s1, e1 in zip(hidden_path, emitted_symbols):
    prob = prob * emission_probs[s1, e1]
print(f'{prob}')

