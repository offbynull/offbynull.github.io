from typing import List

from Graph import Graph
from Read import Read
from WalkRandomEulerianCycle import walk_eulerian_cycle

graph = Graph()
graph.insert_edge(Read('00'), Read('00'))
graph.insert_edge(Read('00'), Read('01'))
graph.insert_edge(Read('01'), Read('10'))
graph.insert_edge(Read('01'), Read('11'))
graph.insert_edge(Read('10'), Read('00'))
graph.insert_edge(Read('10'), Read('01'))
graph.insert_edge(Read('11'), Read('10'))
graph.insert_edge(Read('11'), Read('11'))


def eularian_path_to_kmers(cycle_path: List[Read]) -> List[Read]:
    out = []
    for i in range(len(cycle_path) - 1):
        kmer = cycle_path[i].data + cycle_path[i + 1].data[-1]
        out.append(Read(kmer))
    return out


def do_kmers_cycle(reads: List[Read]) -> bool:
    for i in range(len(reads) - 1):
        if reads[i].suffix() != reads[i + 1].prefix():
            return False
    if reads[-1].suffix() != reads[0].prefix():
        return False
    return True


cycle_path = walk_eulerian_cycle(graph, Read('00'))
cycle_path_as_kmers = eularian_path_to_kmers(cycle_path)
print(f'{cycle_path_as_kmers}')
print(f'{cycle_path_as_kmers[0].stitch(cycle_path_as_kmers)}')
print(f'{do_kmers_cycle(cycle_path_as_kmers)}')
cycle_path = walk_eulerian_cycle(graph, Read('01'))
cycle_path_as_kmers = eularian_path_to_kmers(cycle_path)
print(f'{cycle_path_as_kmers}')
print(f'{cycle_path_as_kmers[0].stitch(cycle_path_as_kmers)}')
print(f'{do_kmers_cycle(cycle_path_as_kmers)}')
cycle_path = walk_eulerian_cycle(graph, Read('10'))
cycle_path_as_kmers = eularian_path_to_kmers(cycle_path)
print(f'{cycle_path_as_kmers}')
print(f'{cycle_path_as_kmers[0].stitch(cycle_path_as_kmers)}')
print(f'{do_kmers_cycle(cycle_path_as_kmers)}')
cycle_path = walk_eulerian_cycle(graph, Read('11'))
cycle_path_as_kmers = eularian_path_to_kmers(cycle_path)
print(f'{cycle_path_as_kmers}')
print(f'{cycle_path_as_kmers[0].stitch(cycle_path_as_kmers)}')
print(f'{do_kmers_cycle(cycle_path_as_kmers)}')

# ['000', '001', '011', '111', '110', '101', '010', '100']
# 0001110100
# True
# ['011', '111', '110', '100', '000', '001', '010', '101']
# 0111000101
# True
# ['100', '000', '001', '010', '101', '011', '111', '110']
# 1000101110
# True
# ['110', '100', '000', '001', '010', '101', '011', '111']
# 1100010111
# True

# The website says accepts the answer of 2, but clearly this is showing that hte answer is 4? starting from each node
# [00, 01, 10, 11], the string that gets generated is always circular -- each kmer appears exactly once and is ordered
# in such a way that it's circular.

# All 4 strings above are just shifted versions of the same string. Maybe what 2 means is that 1 string is the one
# calculated in the code above, and the other string is the reverse of the string? or the complement of that string?

