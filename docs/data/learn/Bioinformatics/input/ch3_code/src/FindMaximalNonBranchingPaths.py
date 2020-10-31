from typing import TypeVar, List, Optional

from Graph import Graph

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


if __name__ == '__main__':
    g = Graph()
    g.insert_edge('1', '2')
    g.insert_edge('2', '3')
    g.insert_edge('2', '4')
    g.insert_edge('2', '5')
    g.insert_edge('4', '6')
    g.insert_edge('4', '10')
    g.insert_edge('5', '7')
    g.insert_edge('6', '10')

    for path in find_maximal_non_branching_paths(g):
        print(f'{"->".join(path)}')
