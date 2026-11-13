# Exercise Break: Prove that for any choice of Spectrum, Graph(Spectrum) is a DAG.
#
# We represent the masses in a spectrum as a sequence Spectrum of integers s1, . . . , sm in increasing order, where s1
# is zero and sm is the total mass of the (unknown) peptide. We define a labeled graph Graph(Spectrum) by forming a node
# for each element of Spectrum, then connecting nodes si and sj by a directed edge labeled by an amino acid a if sj − si
# is equal to the mass of a (see figure below). As we assumed when sequencing antibiotics, we do not distinguish between
# amino acids having the same integer masses (i.e., the pairs K/Q and I/L).

# My answer:
#
# I'm not sure how to prove this. A connection can only go from a lower magnitude node to a higher magnitude node, so
# in that sense, there can never be any cycles. For the possibility of a cycle, a higher magnitude node needs to be
# able to connect to a lower magnitude node (or to a node of the same magnitude). That isn't possible in this case.
