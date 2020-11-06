from collections import Counter
from typing import TypeVar, List, Optional

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph, to_graphviz

T = TypeVar('T')


# MARKDOWN
def walk_until_non_1_to_1(graph: Graph[T], node: T) -> Optional[List[T]]:
    ret = [node]
    ret_quick_lookup = {node}
    while True:
        out_degree = graph.get_out_degree(node)
        in_degree = graph.get_in_degree(node)
        if not(in_degree == 1 and out_degree == 1):
            return ret

        children = graph.get_outputs(node)
        child = next(children)
        if child in ret_quick_lookup:
            return ret

        node = child
        ret.append(node)
        ret_quick_lookup.add(node)


def walk_until_loop(graph: Graph[T], node: T) -> Optional[List[T]]:
    ret = [node]
    ret_quick_lookup = {node}
    while True:
        out_degree = graph.get_out_degree(node)
        if out_degree > 1 or out_degree == 0:
            return None

        children = graph.get_outputs(node)
        child = next(children)
        if child in ret_quick_lookup:
            return ret

        node = child
        ret.append(node)
        ret_quick_lookup.add(node)


def find_maximal_non_branching_paths(graph: Graph[T]) -> List[List[T]]:
    paths = []

    for node in graph.get_nodes():
        out_degree = graph.get_out_degree(node)
        in_degree = graph.get_in_degree(node)
        if (in_degree == 1 and out_degree == 1) or out_degree == 0:
            continue
        for child in graph.get_outputs(node):
            path_from_child = walk_until_non_1_to_1(graph, child)
            if path_from_child is None:
                continue
            path = [node] + path_from_child
            paths.append(path)

    skip_nodes = set()
    for node in graph.get_nodes():
        if node in skip_nodes:
            continue
        out_degree = graph.get_out_degree(node)
        in_degree = graph.get_in_degree(node)
        if not (in_degree == 1 and out_degree == 1) or out_degree == 0:
            continue
        path = walk_until_loop(graph, node)
        if path is None:
            continue
        path = path + [node]
        paths.append(path)
        skip_nodes |= set(path)

    return paths
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input().strip()
                if len(line) > 0:
                    lines.append(line)
            except EOFError:
                break

        command = lines[0]
        lines = lines[1:]
        counter = Counter(lines)
        if command == 'reads':
            frags = [Read(r, i) for r, c in counter.items() for i in range(c)]
        elif command == 'read-pairs':
            frags = [ReadPair(Kdmer(r.split('|')[0], r.split('|')[2], int(r.split('|')[1])), i) for r, c in counter.items() for i in range(c)]
        else:
            raise
        graph = to_debruijn_graph(frags)
        print(f'Given the fragments {lines}, the de Bruijn graph is...', end="\n\n")
        print(f'```{{dot}}\n{to_graphviz(graph)}\n```\n\n')
        print(f'The following contigs were found...', end="\n\n")
        for path in find_maximal_non_branching_paths(graph):
            print(f'{"->".join([str(p) for p in path])}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
# if __name__ == '__main__':
#     g = Graph()
#     g.insert_edge('1', '2')
#     g.insert_edge('2', '3')
#     g.insert_edge('2', '4')
#     g.insert_edge('2', '5')
#     g.insert_edge('4', '6')
#     g.insert_edge('4', '10')
#     g.insert_edge('5', '7')
#     g.insert_edge('6', '10')
#
#     for path in find_maximal_non_branching_paths(g):
#         print(f'{"->".join(path)}')
