from collections import Counter
from math import log
from typing import TypeVar

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph
from helpers.Utils import slide_window


with open('/home/user/Downloads/dataset_240404_4.txt') as f:
    lines = f.read().splitlines(keepends=False)
emitted_seq = list(lines[0])
symbols = lines[2].split()
hidden_path = list(lines[4])
states = lines[6].split()

state_transition_counts = Counter()
total_state_transition_counts = Counter()
for (from_s, to_s), _ in slide_window(hidden_path, 2):
    state_transition_counts[from_s, to_s] += 1
    total_state_transition_counts[from_s] += 1

print(f'\t', end='')
for s in states:
    print(f'{s}\t', end='')
print()
for from_s in states:
    print(f'{from_s}\t', end='')
    for to_s in states:
        full_total = total_state_transition_counts[from_s]
        match_total = state_transition_counts[from_s, to_s]
        if full_total == 0:
            transition_weight = 1.0 / len(states)
        else:
            transition_weight = match_total / full_total
        print(f'{transition_weight}\t', end='')
    print()

print('--------')

state_emission_counts = Counter()
total_state_emission_counts = Counter()
for (state, symbol) in zip(hidden_path, emitted_seq):
    state_emission_counts[state, symbol] += 1
    total_state_emission_counts[state] += 1

print(f'\t', end='')
for s in states:
    print(f'{s}\t', end='')
print()
for state in states:
    for i, symbol in enumerate(symbols):
        if i == 0:
            print(f'{symbol}\t', end='')
        full_total = total_state_emission_counts[state]
        match_total = state_emission_counts[state, symbol]
        if full_total == 0:
            emission_weight = 1.0 / len(symbols)
        else:
            emission_weight = match_total / full_total
        print(f'{emission_weight}\t', end='')
    print()