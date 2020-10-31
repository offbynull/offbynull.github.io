from BalanceNearlyBalancedGraph import balance_graph
from Read import Read
from ToDeBruijnGraph import to_debruijn_graph
from WalkRandomEulerianCycle import walk_eulerian_cycle

with open('/home/user/Downloads/dataset_240261_7(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].strip())
kmers = lines[1:]
kmers = [l.strip() for l in kmers] # get rid of whitespace
kmers = [l for l in kmers if len(l) > 0] # get rid of empty lines

reads = [Read(kmer) for kmer in kmers]
graph = to_debruijn_graph(reads)

graph, roots, tails = balance_graph(graph)

path = walk_eulerian_cycle(graph, roots.pop())
path.pop()  # last conn in cycle is artificial -- it was created from balancing so generating this path would be fast
genome = path[0].stitch(path)
print(f'{genome}')