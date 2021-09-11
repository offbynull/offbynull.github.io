from typing import TypeVar, Any

from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')


# MARKDOWN
def is_simple_tree(g: Graph[N, ND, E, float]) -> bool:
    # Check for cycles
    if len(g) == 0:
        return False
    walked_edges = set()
    walked_nodes = set()
    queued_edges = set()
    start_n = next(g.get_nodes())
    for e in g.get_outputs(start_n):
        queued_edges.add((start_n, e))
    while len(queued_edges) > 0:
        ignore_n, e = queued_edges.pop()
        active_n = [n for n in g.get_edge_ends(e) if n != ignore_n][0]
        walked_edges.add(e)
        walked_nodes.update({ignore_n, active_n})
        children = set(g.get_outputs(active_n))
        children.remove(e)
        for child_e in children:
            if child_e in walked_edges:
                return False  # cyclic -- edge already walked
            child_ignore_n = active_n
            queued_edges.add((child_ignore_n, child_e))
    # Check for disconnected graph
    if len(walked_nodes) != len(g):
        return False  # disconnected -- some nodes not reachable
    # Test degrees
    for n in g.get_nodes():
        # Degree == 1 is leaf node
        # Degree == 2 is a non-splitting internal node (NOT ALLOWED)
        # Degree > 2 is splitting internal node
        degree = g.get_degree(n)
        if degree == 2:
            return False
    # Test weights
    for e in g.get_edges():
        # No non-positive weights
        weight = g.get_edge_data(e)
        if weight <= 0:
            return False
    return True
# MARKDOWN


def create_tree(edges: list[list[Any]]) -> Graph:
    g = Graph()
    for n in {n for e in edges for n in e[:2]}:
        g.insert_node(n)
    for n1, n2, weight in edges:
        g.insert_edge(f'{n1}-{n2}', n1, n2, int(weight))
    return g


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n}\n'
    for e in g.get_edges():
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight}"]\n'
    ret += '}'
    return ret


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        edges, _ = str_to_list(input().strip(), 0)
        g = create_tree(edges)
        print('The graph...')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
        if is_simple_tree(g):
            print('... is a simple tree.')
        else:
            print('... is NOT a simple tree')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()