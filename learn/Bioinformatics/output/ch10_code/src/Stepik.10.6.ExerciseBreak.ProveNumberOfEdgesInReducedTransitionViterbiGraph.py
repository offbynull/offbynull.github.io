# ￼Exercise Break: Let Edges denote the set of edges in the diagram of an HMM that may have some forbidden transitions.
# Prove that the number of edges in the Viterbi graph for this HMM is |Edges| * (n − 1) + 2 * |States|.
#
#    .--.      .--.
#    |  |      |  |
#    '->A----->B<-'
#       ^      |
#       |      v
#    .->D<-----C
#    |  |
#    '--'


# MY ANSWER
# ---------
# 1. Each layer of the Viterbi graph has 1 node for each possible state, and that state has outgoing edges to the next
#    layer matching exactly the transitions in the HMM graph (e.g. A in layer 1 will connect to A and B in layer 2). As
#    such, each layer in the Viterbi graph will have |Edges|.
# 2. Since n symbols being emitted, there are n-1 state transitions occurring / n-1 layers: |Edges|*(n-1)
# 3. There are |States| edges from going to SOURCE to first layer
# 4. There are |States| edges from going to SINK to last layer
#