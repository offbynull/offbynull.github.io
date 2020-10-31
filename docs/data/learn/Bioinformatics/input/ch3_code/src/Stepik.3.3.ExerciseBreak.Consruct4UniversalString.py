from random import shuffle

from Read import Read
from ToOverlapGraphHash import to_overlap_graph
from Utils import enumerate_patterns

segments = [Read(segment) for segment in enumerate_patterns(4, '01')]
print(f'{segments}')

graph = to_overlap_graph(segments)

graph_items_randomized = list(graph.get_all_outputs())
shuffle(graph_items_randomized)
for segment, other_segments in graph_items_randomized:
    other_segments = list(other_segments)
    print(f'{segment} -> {",".join([str(x) for x in other_segments])}')


def walk(path):
    if len(path) == len(graph):
        print(f'{path} -> {path[0].stitch(path)}')
        return

    n = path[-1]
    for child_n in graph.get_outputs(n):
        if child_n not in path:
            path.append(child_n)
            walk(path)
            path.pop()


for node in graph.get_nodes():
    walk([node])