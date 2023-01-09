import math
from builtins import sorted
from collections import defaultdict, Counter
from itertools import product

from graph import DirectedGraph
from graph.GraphHelpers import StringIdGenerator

# Exercise Break: Construct the 27 × 20 emission probability matrix for HMM(Alignment, 0.35) derived from the multiple
# alignment that we have been using as an example, reproduced below.
#
#
# M1  M2  M3  M4  M5  I5  M6  M7  M8
# A   C   D   E   F   AC  A   D   F
# A   F   D   A   -   --  C   C   F
# A   -   -   E   F   D-  F   D   C
# A   C   A   E   F   --  A   -   C
# A   D   D   E   F   AA  A   D   F

# MY ANSWER
# ---------
# Where does the 27x20 come from? There are 27 nodes in total in the state transition graph of the book. There are 20
# amino acids in total.
amino_acids = 'ARNDCQEGHILKMFPSTWYV'
n = 8
match_list = {
    1: 'AAAAA',
    2: 'CFCD',
    3: 'DDAD',
    4: 'EAEEE',
    5: 'FFFF',
    6: 'ACFAA',
    7: 'DCDD',
    8: 'FFCCF'
}
insert_list = {
    0: '',
    1: '',
    2: '',
    3: '',
    4: '',
    5: 'ADACA',
    6: '',
    7: '',
    8: ''
}
delete_list = {
    1: '',
    2: '',
    3: '',
    4: '',
    5: '',
    6: '',
    7: '',
    8: ''
}

probs = defaultdict(lambda: 0.0)

for i in range(1, n+1):
    total = len(match_list[i])
    counts = Counter(match_list[i])
    for ch in amino_acids:
        print(f'Emission at M{i} for {ch} : {counts[ch] / total if total != 0 else 0}')
for i in range(n+1):
    total = len(insert_list[i])
    counts = Counter(insert_list[i])
    for ch in amino_acids:
        print(f'Emission at I{i} for {ch} : {counts[ch] / total if total != 0 else 0}')
for i in range(1, n+1):
    total = len(delete_list[i])
    counts = Counter(delete_list[i])
    for ch in amino_acids:
        print(f'Emission at D{i} for {ch} : {counts[ch] / total if total != 0 else 0}')

# Emissions for the source node (S) and sink node (E) are omitted, because they can't emit anything (all 0 emission
# probabilities). If you add them in (20 each), you'll get exactly 27*20=540 emission probabilities, which is what the
# quesiton is asking for.
