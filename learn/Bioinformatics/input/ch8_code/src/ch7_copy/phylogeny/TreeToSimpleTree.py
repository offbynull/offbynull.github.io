from typing import TypeVar, Any

from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')


def create_graph(edges: list[list[Any]]) -> Graph:
    g = Graph()
    for n in {n for e in edges for n in e[:2]}:
        g.insert_node(n)
    for n1, n2, weight in edges:
        g.insert_edge(f'{n1}-{n2}', n1, n2, float(weight))
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


# MARKDOWN_TREE_TEST
def is_tree(g: Graph[N, ND, E, float]) -> bool:
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
    return True


def is_simple_tree(g: Graph[N, ND, E, float]) -> bool:
    # Check if tree
    if not is_tree(g):
        return False
    # Test degrees
    for n in g.get_nodes():
        # Degree == 0 shouldn't exist if tree
        # Degree == 1 is leaf node
        # Degree == 2 is a non-splitting internal node (NOT ALLOWED)
        # Degree >= 3 is splitting internal node
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
# MARKDOWN_TREE_TEST


# MARKDOWN
def merge_nodes_of_degree2(g: Graph[N, ND, E, float]) -> None:
    # Can be made more efficient by not having to re-collect bad nodes each
    # iteration. Kept it like this so it's simple to understand what's going on.
    while True:
        bad_nodes = {n for n in g.get_nodes() if g.get_degree(n) == 2}
        if len(bad_nodes) == 0:
            return
        bad_n = bad_nodes.pop()
        bad_e1, bad_e2 = tuple(g.get_outputs(bad_n))
        e_id = bad_e1 + bad_e2
        e_n1 = [n for n in g.get_edge_ends(bad_e1) if n != bad_n][0]
        e_n2 = [n for n in g.get_edge_ends(bad_e2) if n != bad_n][0]
        e_weight = g.get_edge_data(bad_e1) + g.get_edge_data(bad_e2)
        g.insert_edge(e_id, e_n1, e_n2, e_weight)
        g.delete_edge(bad_e1)
        g.delete_edge(bad_e2)
        g.delete_node(bad_n)
# MARKDOWN


def main_simplify():
    edges, _ = str_to_list(input().strip(), 0)
    g = create_graph(edges)
    assert is_tree(g)  # Ensure graph is a tree
    print('The tree...')
    print()
    print('```{dot}')
    print(f'{to_dot(g)}')
    print('```')
    print()
    print('... simplifies to ...')
    merge_nodes_of_degree2(g)
    print()
    print('```{dot}')
    print(f'{to_dot(g)}')
    print('```')
    print()


def main_test():
    edges, _ = str_to_list(input().strip(), 0)
    g = create_graph(edges)
    assert is_tree(g)  # Ensure graph is a tree
    print('The tree...')
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


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        opt = input().strip()
        if opt == 'simplify':
            main_simplify()
        elif opt == 'test':
            main_test()
        else:
            raise ValueError('???')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()