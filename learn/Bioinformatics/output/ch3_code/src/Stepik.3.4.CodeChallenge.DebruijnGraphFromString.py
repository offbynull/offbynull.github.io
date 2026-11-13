from Read import Read
from ToDeBruijnGraph import to_debruijn_graph
from Utils import slide_window

with open('/home/user/Downloads/dataset_240257_6(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].strip())
dna = lines[1].strip()

reads = [Read(kmer) for kmer, _ in slide_window(dna, k)]

graph = to_debruijn_graph(reads)
for node, other_nodes in graph.get_all_outputs():
    other_nodes = list(other_nodes)
    if len(other_nodes) == 0:
        continue
    print(f'{node} -> {",".join([str(x) for x in other_nodes])}')