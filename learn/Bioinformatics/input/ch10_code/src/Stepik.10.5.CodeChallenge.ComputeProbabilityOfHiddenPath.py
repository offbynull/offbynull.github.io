from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240399_8.txt') as f:
    lines = f.read().splitlines(keepends=False)
seq = lines[0]
states = lines[2].split()
transition_probs = {}
mat_head = lines[4].split()
for mat_row in lines[5:]:
    mat_row = mat_row.split()
    state1 = mat_row[0]
    for i, state2 in enumerate(mat_head):
        transition_probs[state1, state2] = float(mat_row[i+1])

prob = 1.0 / len(states)
for (s1, s2), _ in slide_window(seq, 2):
    prob = prob * transition_probs[s1, s2]
print(f'{prob}')

