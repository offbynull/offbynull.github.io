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
from itertools import product

from GraphGridCreate import create_grid_graph
from PopulateWeightsAndBacktrackPointers_DynamicProgramming import populate_weights_and_backtrack_pointers

with open('Marahiel_data.csv', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = data.strip().split('\n')
sequences = [list(s) for s in lines[1:]]

for s1, s2 in product(sequences, repeat=2):
    if s1 is s2:
        continue
    graph = create_grid_graph(
        [s1, s2],
        lambda n: (True, (None, None)),
        lambda e, _1, offset, _2: (True, offset == (1,1))
    )
    populate_weights_and_backtrack_pointers(
        graph,
        (0, 0),
        lambda n, weight, backtracking_edge: graph.update_node_data(n, (weight, backtracking_edge)),
        lambda n: graph.get_node_data(n),
        lambda e: graph.get_edge_data(e)
    )
    print('!')