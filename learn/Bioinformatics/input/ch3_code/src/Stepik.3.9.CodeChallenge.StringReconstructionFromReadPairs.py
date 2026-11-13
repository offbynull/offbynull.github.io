from BalanceNearlyBalancedGraph import balance_graph
from ReadPair import ReadPair
from Kdmer import Kdmer
from ToOverlapGraphHash import to_overlap_graph
from WalkRandomEulerianCycle import walk_eulerian_cycle

with open('/home/user/Downloads/dataset_240262_16(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()


lines = data.split('\n')
lines = [l.strip() for l in lines]  # get rid of whitespace
lines = [l for l in lines if len(l) > 0]  # get rid of empty li

k, d = [int(s) for s in lines[0].split(' ')]

kdmers = [tuple(s.split('|', maxsplit=2)) for s in lines[1:]]
kdmers = [Kdmer(k1, k2, d) for k1, k2 in kdmers]
read_pairs = [ReadPair(kdmer) for kdmer in kdmers]

graph = to_overlap_graph(read_pairs)
graph, roots, tails = balance_graph(graph)
path = walk_eulerian_cycle(
    graph,
    list(roots)[0]
)
path.pop()  # remove last kdmer because the cycle we created when balancing the graph is artificial -- we just did it so
            # we can get the path using eularian cycles, which is an efficient way of reconstructing the string.

genome = path[0].stitch(path)
print(f'{genome}')