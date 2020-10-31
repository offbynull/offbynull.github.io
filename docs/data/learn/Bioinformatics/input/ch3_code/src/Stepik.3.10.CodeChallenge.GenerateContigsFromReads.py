from FindMaximalNonBranchingPaths import find_maximal_non_branching_paths
from Read import Read
from ToDeBruijnGraph import to_debruijn_graph

with open('/home/user/Downloads/dataset_240263_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmers = lines[:]
kmers = [l.strip() for l in kmers] # get rid of whitespace
kmers = [l for l in kmers if len(l) > 0] # get rid of empty lines

reads = [Read(kmer) for kmer in kmers]

graph = to_debruijn_graph(reads)
contigs = find_maximal_non_branching_paths(graph)
for contig in contigs:
    output = contig[0].stitch(contig)
    print(f'{output}')