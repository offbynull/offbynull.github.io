from FindMaximalNonBranchingPaths import find_maximal_non_branching_paths
from Graph import Graph

with open('/home/user/Downloads/dataset_240267_2(3).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
adjacency_list = lines[:]
adjacency_list = [l.strip() for l in adjacency_list] # get rid of whitespace
adjacency_list = [l for l in adjacency_list if len(l) > 0] # get rid of empty lines
adjacency_list = [l.split(' -> ') for l in adjacency_list]
adjacency_list = [(l[0], l[1].split(',')) for l in adjacency_list]

graph = Graph()
[graph.insert_edge(from_node, to_node) for from_node, to_nodes in adjacency_list for to_node in to_nodes]

paths = find_maximal_non_branching_paths(graph)
for path in find_maximal_non_branching_paths(graph):
    print(f'{"->".join(path)}')