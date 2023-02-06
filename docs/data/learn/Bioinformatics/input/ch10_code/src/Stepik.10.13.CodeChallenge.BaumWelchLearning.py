from collections import defaultdict

from hmm.CertaintyOfEmittedSequenceTravelingThroughHiddenPathEdge import edge_certainties
from hmm.CertaintyOfEmittedSequenceTravelingThroughHiddenPathNode import node_certainties
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import to_hmm_graph_PRE_PSEUDOCOUNTS

with open('/home/user/Downloads/dataset_240406_5.txt') as f:
    lines = f.read().splitlines(keepends=False)
iterations = int(lines[0])
emitted_seq = list(lines[2])
symbols = lines[4].split()
states = lines[6].split()
mat_head = lines[8].split()
state_transition_probs = defaultdict(dict)
for mat_row in lines[9:9+len(states)]:
    mat_row = mat_row.split()
    state = mat_row[0]
    for i, to_state in enumerate(mat_head):
        state_transition_probs[state][to_state] = float(mat_row[i + 1])
state_emission_probs = defaultdict(dict)
mat_head = lines[9+len(states)+1].split()
for mat_row in lines[9+len(states)+2:]:
    mat_row = mat_row.split()
    state = mat_row[0]
    for i, symbol in enumerate(mat_head):
        state_emission_probs[state][symbol] = float(mat_row[i + 1])


for _ in range(iterations):
    for st in states:
        state_transition_probs['SOURCE'][st] = 1.0 / len(states)
    hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(state_transition_probs, state_emission_probs)
    _, _, f_exploded_n_certainties = node_certainties(hmm, 'SOURCE', 'SINK', emitted_seq)
    _, _, f_exploded_e_certainties = edge_certainties(hmm, 'SOURCE', 'SINK', emitted_seq)

    transition_sums = defaultdict(lambda: 0.0)
    for (f_exploded_from_n_id, f_exploded_to_n_id), certainty in f_exploded_e_certainties.items():
        _, hmm_from_n_id = f_exploded_from_n_id
        _, hmm_to_n_id = f_exploded_to_n_id
        if hmm_from_n_id == 'SOURCE' or hmm_to_n_id == 'SINK':
            continue
        transition_sums[hmm_from_n_id, hmm_to_n_id] += certainty
        # print(f'{f_exploded_from_n_id, f_exploded_to_n_id, certainty}')
    # print(f'{transition_sums}')

    emission_sums = defaultdict(lambda: 0.0)
    for expected_symbol in symbols:
        for f_exploded_to_n_id, certainty in f_exploded_n_certainties.items():
            f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
            if hmm_to_n_id == 'SOURCE' or hmm_to_n_id == 'SINK':
                continue
            symbol = emitted_seq[f_exploded_to_n_emission_idx]
            if symbol != expected_symbol:
                continue
            emission_sums[hmm_to_n_id, symbol] += certainty
            # print(f'{f_exploded_from_n_id, f_exploded_to_n_id, certainty}')
    # print(f'{emission_sums}')

    # normalize
    new_state_transition_probs = defaultdict(lambda: defaultdict(lambda: 0.0))
    for s1, s2 in transition_sums:
        total = sum(transition_sums[s1, s] for s in states)
        new_state_transition_probs[s1][s2] = transition_sums[s1, s2] / total
    # print(f'{new_state_transition_probs}')

    new_state_emissions_probs = defaultdict(lambda: defaultdict(lambda: 0.0))
    for st, sym in emission_sums:
        total = sum(emission_sums[st, s] for s in symbols)
        new_state_emissions_probs[st][sym] = emission_sums[st, sym] / total
    # print(f'{new_state_emissions_probs}')

    state_transition_probs = new_state_transition_probs
    state_emission_probs = new_state_emissions_probs


print(f'\t', end='')
for from_state in states:
    print(f'{from_state}\t', end='')
print()
for from_state in states:
    print(f'{from_state}\t', end='')
    for to_state in states:
        print(f'{state_transition_probs[from_state][to_state]}\t', end='')
    print()

print('--------')

print(f'\t', end='')
for symbol in symbols:
    print(f'{symbol}\t', end='')
print()
for from_state in states:
    for i, symbol in enumerate(symbols):
        if i == 0:
            print(f'{from_state}\t', end='')
        print(f'{state_emission_probs[from_state][symbol]}\t', end='')
    print()

