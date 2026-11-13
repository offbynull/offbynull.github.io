from collections import Counter
from typing import List, Tuple, TypeVar, Set

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph, to_graphviz
from WalkRandomEulerianCycle import walk_eulerian_cycle

T = TypeVar('T')


# MARKDOWN
def find_unbalanced_nodes(graph: Graph[T]) -> List[Tuple[T, int, int]]:
    unbalanced_nodes = []
    for node in graph.get_nodes():
        in_degree = graph.get_in_degree(node)
        out_degree = graph.get_out_degree(node)
        if in_degree != out_degree:
            unbalanced_nodes.append((node, in_degree, out_degree))
    return unbalanced_nodes


# creates a balanced graph from a nearly balanced graph -- nearly balanced means the graph has an equal number of
# missing outputs and missing inputs.
def balance_graph(graph: Graph[T]) -> Tuple[Graph[T], Set[T], Set[T]]:
    unbalanced_nodes = find_unbalanced_nodes(graph)
    nodes_with_missing_ins = filter(lambda x: x[1] < x[2], unbalanced_nodes)
    nodes_with_missing_outs = filter(lambda x: x[1] > x[2], unbalanced_nodes)

    graph = graph.copy()

    # create 1 copy per missing input / per missing output
    n_per_need_in = [_n for n, in_degree, out_degree in nodes_with_missing_ins for _n in [n] * (out_degree - in_degree)]
    n_per_need_out = [_n for n, in_degree, out_degree in nodes_with_missing_outs for _n in [n] * (in_degree - out_degree)]
    assert len(n_per_need_in) == len(n_per_need_out)  # need an equal count of missing ins and missing outs to balance

    # balance
    for n_need_in, n_need_out in zip(n_per_need_in, n_per_need_out):
        graph.insert_edge(n_need_out, n_need_in)

    return graph, set(n_per_need_in), set(n_per_need_out)  # return graph with cycle, orig root nodes, orig tail nodes
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
        graph, head_nodes, tail_nodes = balance_graph(graph)
        print(f'Given the fragments {lines}, the artificially balanced de Bruijn graph is...', end="\n\n")
        print(f'```{{dot}}\n{to_graphviz(graph)}\n```\n\n')
        print(f'... with original head nodes at {head_nodes} and tail nodes at {tail_nodes}.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     g = Graph()
#     g.insert_edge('0', '2')
#     g.insert_edge('1', '3')
#     g.insert_edge('2', '1')
#     g.insert_edge('3', '0')
#     g.insert_edge('3', '4')
#     g.insert_edge('6', '3')
#     g.insert_edge('6', '7')
#     g.insert_edge('7', '8')
#     g.insert_edge('8', '9')
#     g.insert_edge('9', '6')
#
#     g, _, _ = balance_graph(g)
#     path = walk_eularian_cycle(g, '0')
#     print(f'{"->".join(path)}')
