from ToDeBruijnGraph import to_debruijn_graph
from Read import Read

with open('/home/user/Downloads/dataset_240258_8(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmers = lines[:]
kmers = [l.strip() for l in kmers] # get rid of whitespace
kmers = [l for l in kmers if len(l) > 0] # get rid of empty lines

reads = [Read(kmer) for kmer in kmers]

graph = to_debruijn_graph(reads)
for node, other_nodes in graph.get_all_outputs():
    other_nodes = list(other_nodes)
    if len(other_nodes) == 0:
        continue
    print(f'{node} -> {",".join([str(x) for x in other_nodes])}')