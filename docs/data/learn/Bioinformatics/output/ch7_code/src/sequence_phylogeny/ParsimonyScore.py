from typing import TypeVar, Callable, Any

from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')


def create_graph(elems: list[list[Any]]) -> Graph:
    g = Graph()
    for e in elems:
        if e[0] == 'n':
            g.insert_node(e[1], e[2])
        if e[0] == 'e':
            g.insert_edge(f'{e[1]}-{e[2]}', e[1], e[2], {})
    return g


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=BT]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        seq = g.get_node_data(n)
        ret += f'{n} [label="{n}\\n{seq}"]\n'
    for e in g.get_edges():
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight.get("w")}"]\n'
    ret += '}'
    return ret


def hamming_distance(kmer1: str, kmer2: str) -> int:
    mismatch = 0
    for ch1, ch2 in zip(kmer1, kmer2):
        if ch1 != ch2:
            mismatch += 1
    return mismatch


# MARKDOWN
def populate_edge_similarity(
        g: Graph[N, ND, E, ED],
        get_sequence: Callable[[ND], str],
        set_weight: Callable[[ED, float], None]
) -> None:
    for e in g.get_edges():
        n1, n2, e_data = g.get_edge(e)
        n1_data = g.get_node_data(n1)
        n2_data = g.get_node_data(n2)
        n1_seq = get_sequence(n1_data)
        n2_seq = get_sequence(n2_data)
        weight = hamming_distance(n1_seq, n2_seq)
        set_weight(e_data, weight)


def parsimony_score(
        g: Graph[N, ND, E, ED],
        get_weight: Callable[[ED], float]
) -> float:
    ret = 0.0
    for e in g.get_edges():
        e_data = g.get_edge_data(e)
        ret += get_weight(e_data)
    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        elems, _ = str_to_list(input().strip(), 0)
        g = create_graph(elems)
        print('The tree...')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
        print('... has a parsimony score of ...')
        populate_edge_similarity(
            g,
            lambda nd: nd,
            lambda ed, weight: ed.__setitem__('w', weight)
        )
        score = parsimony_score(g, lambda ed: ed['w'])
        print()
        print(f'{score}')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()