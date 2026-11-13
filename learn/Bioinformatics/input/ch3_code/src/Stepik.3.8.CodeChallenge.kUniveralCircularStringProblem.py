from Read import Read
from ToDeBruijnGraph import to_debruijn_graph
from Utils import enumerate_patterns
from WalkRandomEulerianCycle import walk_eulerian_cycle

with open('/home/user/Downloads/dataset_240261_11(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0])

reads = [Read(s) for s in enumerate_patterns(k, '01')]
graph = to_debruijn_graph(reads)
path = walk_eulerian_cycle(graph, next(graph.get_nodes()))
k_universal_str = path[0].stitch(path)
print(k_universal_str)