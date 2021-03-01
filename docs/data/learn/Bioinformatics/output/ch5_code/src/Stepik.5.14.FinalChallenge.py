# Options for this:
#
# 1. Pick 2 random seqs and perform a global alignment using PAM250 or BLOSUM62. Then, generate profile matrix as shown
#    in section 5.14. Once that's done, pick a 3rd seq at random and build out a sequence alignment graph using the
#    profile matrix.
#
#    For example, the following profile matrix...
#    A:  .2 .0 .8
#    C:  .1 .0 .0
#    G:  .0 .7 .0
#    T:  .6 .0 .0
#
#    ... and the string GGGG would create the following graph ...
#
#      G G G G
#     o o o o o
#    T
#     o o o o o
#    G
#     o o o o o
#    A
#     o o o o o
#
#    The most frequent item was picked from each column of the profile matrix to generate the consensus string, which is
#    is being as the string to align against.
#
#
#  2. Can you devise an alt form of graph based on the profile? For example, same string and profile as 1, but rather
#     than a normal global alignment graph based on the consensus string, it'd be a graph where each element of the
#     string would have 5 edges coming out of it: one for each nucleotides + gap (ACTG-). Each edge points to the next
#     node for the string.
#
#      G G G G
#     o o o o o
#
#     What defines which edge is taken? The score of the element pair weighed by the frequency.
#
# 3. Use the profile matrix to determine edge weights for each column as well as gaps. Then construct your graph as
#    such...
#
#      G G G G
#     o-o-o-o-o
#    ?|\|\|\|\|
#     o-o-o-o-o
#    ?|\|\|\|\|
#     o-o-o-o-o
#    ?|\|\|\|\|
#     o-o-o-o-o
#    ?|\|\|\|\|
#     o-o-o-o-o
#
#    The columns are the string being tested and the rows are columns from the profile matrix. The graph does global
#    sequence alignment against the profile matrix, taking the weights from each column of the profile matrix. The
#    highest weighted path is the one you want.
#
#    If the alignment results in the profile matrix having a gap, add the gaps in. Then update the frequencies in the
#    profile matrix based on this alignment.
#
#    Maybe penalize the widening of the profile more than widening the sequence.
import json
import time
from itertools import combinations
from os.path import expanduser
from typing import Dict, List

from global_alignment import GlobalAlignment_Matrix, GlobalMultipleAlignment_Matrix, GlobalMultipleAlignment_Greedy
from scoring.SumOfPairsWeightLookup import SumOfPairsWeightLookup
from scoring.WeightLookup import Table2DWeightLookup

####
#### GET BEST PAIRWISE ALIGNMENTS
####
# with open('Marahiel_data.csv', mode='r', encoding='utf-8') as f:
#     data = f.read()
# lines = data.strip().split('\n')
# lines = lines[1:]  # remove header
# lines = set(lines)  # remove dupes (they exist)
# sequences = [list(s.upper()) for s in lines]
#
# weight_lookup = Table2DWeightLookup.create_from_2d_matrix_file('BLOSUM62.txt', -5)
# start = time.time()
# scores = {}
# highest_res = None
# highest_seq_pair = None
# for i, (s1, s2) in enumerate(combinations(sequences, r=2)):
#     if s1 is s2:
#         continue
#     res = GlobalAlignment_Matrix.global_alignment(s1, s2, weight_lookup)
#     if highest_res is None or res[0] > highest_res[0]:
#         highest_res = res
#         highest_seq_pair = (s1, s2)
#         print(f'{res[0]} higher: {("".join(s1))} vs {("".join(s2))}')
#     else:
#         print(f'{res[0]} lower')
#     scores.setdefault(res[0], []).append([s1, s2])
# end = time.time()
#
# for k, v in scores.items():
#     for pair in v:
#         pair[0] = ''.join(pair[0])
#         pair[1] = ''.join(pair[1])
# with open(expanduser('~/output.json'), 'w') as f:
#     f.write(json.dumps(scores, indent=2))
#
# print(f'{highest_res}')
# print(f'{highest_seq_pair[0]}')
# print(f'{highest_seq_pair[1]}')
# print(f'{end - start}')


####
#### TRY TO ALIGN TOP PAIR-WISE ALIGNED SEQUENCES
####
# with open(expanduser('~/output.json'), 'r') as f:
#     pairwise_results: Dict[str, List[List[str]]] = json.load(f)
#
# keys = [float(f) for f in pairwise_results.keys()]
# keys.sort(reverse=True)
# top_pairwise_alignments = [v for k in keys for v in pairwise_results[str(k)]]
# top_pairwise_alignments = top_pairwise_alignments[:20]
#
# weight_lookup_2way = Table2DWeightLookup.create_from_2d_matrix_file('BLOSUM62.txt', -5)
# weight_lookup_final = SumOfPairsWeightLookup(weight_lookup_2way)
# seqs = [list(s) for s in set(s for p in top_pairwise_alignments for s in p)]
# weight, elems = GlobalMultipleAlignment_Greedy.global_alignment(seqs, weight_lookup_2way, weight_lookup_final)


with open('Marahiel_data.csv', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = data.strip().split('\n')
lines = lines[1:]  # remove header
lines = set(lines)  # remove dupes (they exist)
seqs = [list(s.upper()) for s in lines]

weight_lookup_2way = Table2DWeightLookup.create_from_2d_matrix_file('BLOSUM62.txt', -5)
weight_lookup_final = SumOfPairsWeightLookup(weight_lookup_2way)
weight, elems = GlobalMultipleAlignment_Greedy.global_alignment(seqs, weight_lookup_2way, weight_lookup_final)


dims = len(seqs)
for i in range(dims):
    print(f'{"".join("-" if e[i] is None else e[i] for e in elems)}')
print(f'{weight}')
