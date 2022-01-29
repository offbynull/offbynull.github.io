from itertools import combinations, product
from typing import TypeVar, Callable, Any, Optional

from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from ch7_copy.sequence_phylogeny.SmallParsimony import populate_distance_sets

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')


def create_graph(elems: list[list[Any]]) -> Graph[str, dict[str, Any], str, dict[str, Any]]:
    g = Graph()
    for e in elems:
        if e[0] == 'n':
            if len(e) == 3:
                g.insert_node(e[1], {'seq': e[2]})
            else:
                g.insert_node(e[1], {})
        if e[0] == 'e':
            g.insert_edge(f'{e[1]}-{e[2]}', e[1], e[2], {})
    return g


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=BT]\n'
    ret += ' node[shape=box, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    ret += ' layout=fdp\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        nd = g.get_node_data(n)
        nd_str = '\n'.join(f'{k}: {v}' for k, v in nd.items()).replace('\n', '\\n').replace('"', '\\"')
        ret += f'{n} [label="{n}\\n{nd_str}"]\n'
    for e in g.get_edges():
        n1, n2, ed = g.get_edge(e)
        ed_str = '\n'.join(f'{k}: {v}' for k, v in ed.items()).replace('\n', '\\n').replace('"', '\\"')
        ret += f'{n1} -- {n2} [label="{ed_str}"]\n'
    ret += '}'
    return ret


# MARKDOWN_SWAP
def list_nn_swap_options(
        tree: Graph[N, ND, E, ED],
        edge: E
) -> set[
    tuple[
        frozenset[E],  # side1 edges
        frozenset[E]   # side2 edges
    ]
]:
    n1, n2 = tree.get_edge_ends(edge)
    n1_edges = set(tree.get_outputs(n1))
    n2_edges = set(tree.get_outputs(n2))
    n1_edges.remove(edge)
    n2_edges.remove(edge)
    n1_edges = frozenset(n1_edges)
    n2_edges = frozenset(n2_edges)
    n1_edge_cnt = len(n1_edges)
    n2_edge_cnt = len(n2_edges)
    both_edges = n1_edges | n2_edges
    ret = set()
    for n1_edges_perturbed in combinations(both_edges, n1_edge_cnt):
        n1_edges_perturbed = frozenset(n1_edges_perturbed)
        n2_edges_perturbed = frozenset(both_edges.difference(n1_edges_perturbed))
        if (n1_edges_perturbed, n2_edges_perturbed) in ret:
            continue
        if (n2_edges_perturbed, n1_edges_perturbed) in ret:
            continue
        if {n1_edges_perturbed, n2_edges_perturbed} == {n1_edges, n2_edges}:
            continue
        ret.add((n1_edges_perturbed, n2_edges_perturbed))
    return ret


def nn_swap(
    tree: Graph[N, ND, E, ED],
    edge: E,
    side1: frozenset[E],
    side2: frozenset[E]
) -> tuple[
    frozenset[E],  # orig edges for side A
    frozenset[E]   # orig edges for side B
]:
    n1, n2 = tree.get_edge_ends(edge)
    n1_edges = set(tree.get_outputs(n1))
    n2_edges = set(tree.get_outputs(n2))
    n1_edges.remove(edge)
    n2_edges.remove(edge)
    assert n1_edges | n2_edges == side1 | side2
    edge_details = {}
    for e in side1 | side2:
        end1, end2, data = tree.get_edge(e)
        end = {end1, end2}.difference({n1, n2}).pop()
        edge_details[e] = (end, data)
        tree.delete_edge(e)
    for e in side1:
        end, data = edge_details[e]
        tree.insert_edge(e, n1, end, data)
    for e in side2:
        end, data = edge_details[e]
        tree.insert_edge(e, n2, end, data)
    return frozenset(n1_edges), frozenset(n2_edges)  # return original edges
# MARKDOWN_SWAP


# MARKDOWN_SCORE
def parsimony_score(
        tree: Graph[N, ND, E, ED],
        seq_length: int,
        get_dist_set: Callable[
            [
                N,  # node
                int  # index within N's sequence
            ],
            dict[str, float]
        ],
        set_edge_score: Callable[[E, float], None],
        dist_metric: Callable[[str, str], float]
) -> float:
    total_score = 0.0
    edges = set(tree.get_edges())  # iterator to set -- avoids concurrent modification bug
    for e in edges:
        n1, n2 = tree.get_edge_ends(e)
        e_score = 0.0
        for idx in range(seq_length):
            n1_ds = get_dist_set(n1, idx)
            n2_ds = get_dist_set(n2, idx)
            n1_elem = min(n1_ds, key=lambda k: n1_ds[k])
            n2_elem = min(n2_ds, key=lambda k: n2_ds[k])
            e_score += dist_metric(n1_elem, n2_elem)
        set_edge_score(e, e_score)
        total_score += e_score
    return total_score
# MARKDOWN_SCORE


# MARKDOWN
def nn_interchange(
        tree: Graph[N, ND, E, ED],
        root: N,
        seq_length: int,
        get_sequence: Callable[[N], str],
        set_sequence: Callable[[N, str], None],
        get_dist_set: Callable[
            [
                N,  # node
                int  # index within N's sequence
            ],
            dict[str, float]
        ],
        set_dist_set: Callable[
            [
                N,  # node
                int,  # index within N's sequence
                dict[str, float]
            ],
            None
        ],
        dist_metric: Callable[[str, str], float],
        set_edge_score: Callable[[E, float], None],
        elem_types: str = 'ACTG',
        update_callback: Optional[Callable[[Graph, float], None]] = None
) -> tuple[float, float]:
    input_score = None
    output_score = None
    while True:
        populate_distance_sets(
            tree,
            root,
            seq_length,
            get_sequence,
            set_sequence,
            get_dist_set,
            set_dist_set,
            dist_metric,
            elem_types
        )
        orig_score = parsimony_score(
            tree,
            seq_length,
            get_dist_set,
            set_edge_score,
            dist_metric
        )
        if input_score is None:
            input_score = orig_score
        output_score = orig_score
        if update_callback is not None:
            update_callback(tree, output_score)  # notify caller that the graph updated
        swap_scores = []
        edges = set(tree.get_edges())  # bug -- avoids concurrent modification problems
        for edge in edges:
            # is it a limb? if so, skip it -- we want internal edges only
            n1, n2 = tree.get_edge_ends(edge)
            if tree.get_degree(n1) == 1 or tree.get_degree(n2) == 1:
                continue
            # get all possible nn swaps for this internal edge
            options = list_nn_swap_options(tree, edge)
            # for each possible swap...
            for swapped_side1, swapped_side2 in options:
                # swap
                orig_side1, orig_side2 = nn_swap(
                    tree,
                    edge,
                    swapped_side1,
                    swapped_side2
                )
                # small parsimony
                populate_distance_sets(
                    tree,
                    root,
                    seq_length,
                    get_sequence,
                    set_sequence,
                    get_dist_set,
                    set_dist_set,
                    dist_metric,
                    elem_types
                )
                # score and store
                score = parsimony_score(
                    tree,
                    seq_length,
                    get_dist_set,
                    set_edge_score,
                    dist_metric
                )
                swap_scores.append((score, edge, swapped_side1, swapped_side2))
                # unswap (back to original tree)
                nn_swap(
                    tree,
                    edge,
                    orig_side1,
                    orig_side2
                )
        # if swap producing the lowest parsimony score is lower than original, apply that
        # swap and try again, otherwise we're finished
        score, edge, side1, side2 = min(swap_scores, key=lambda x: x[0])
        if score >= orig_score:
            return input_score, output_score
        else:
            nn_swap(tree, edge, side1, side2)
# MARKDOWN





def main_nn_swap():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        g_as_list, _ = str_to_list(input().strip(), 0)
        edge = input().strip()
        g = create_graph(g_as_list)
        print(f'The tree...')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
        print(f'... can have any of the following nearest neighbour swaps on edge {edge}...')
        print()
        opts = list_nn_swap_options(g, edge)
        for side1, side2 in opts:
            orig1, orig2 = nn_swap(g, edge, side1, side2)
            print()
            print('```{dot}')
            print(f'{to_dot(g)}')
            print('```')
            print()
            nn_swap(g, edge, orig1, orig2)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


def main_parsimony_score():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        g_as_list, _ = str_to_list(input().strip(), 0)
        root = input().strip()
        dist_mat = {}
        table_header, _ = str_to_list(input().strip(), 0)
        table_rows = []
        for _ in table_header[1:]:
            row, _ = str_to_list(input().strip(), 0)
            table_rows.append(row)
        for row in table_rows:
            e1 = row[0]
            for i, e2 in enumerate(table_header[1:]):
                dist_mat[e1, e2] = float(row[i + 1])
        elem_types = table_header[1:]
        g = create_graph(g_as_list)
        leaf_nodes = {n for n in g.get_nodes() if g.get_degree(n) == 1}
        leaf_node = next(iter(leaf_nodes))
        seq_length = len(g.get_node_data(leaf_node)['seq'])
        print('The tree...')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
        populate_distance_sets(
            g,
            root,
            seq_length,
            lambda n: g.get_node_data(n)['seq'],
            lambda n, seq: g.get_node_data(n).update({'seq': seq}),
            lambda n, idx: g.get_node_data(n).get(f'dist_set_{idx}', {}),
            lambda n, idx, ds: g.get_node_data(n).update({f'dist_set_{idx}': ds}),
            lambda e1, e2: dist_mat[e1, e2],
            elem_types
        )
        score = parsimony_score(
            g,
            seq_length,
            lambda n, idx: g.get_node_data(n).get(f'dist_set_{idx}', {}),
            lambda e, score: g.get_edge_data(e).update({'score': score}),
            lambda e1, e2: dist_mat[e1, e2]
        )
        # remove dist_sets so that the output dot graph is uncluttered
        for n, idx in product(g.get_nodes(), range(seq_length)):
            g.get_node_data(n).pop(f'dist_set_{idx}')
        print()
        print(f'... has a parsimony score of {score}...')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        g_as_list, _ = str_to_list(input().strip(), 0)
        root = input().strip()
        dist_mat = {}
        table_header, _ = str_to_list(input().strip(), 0)
        table_rows = []
        for _ in table_header[1:]:
            row, _ = str_to_list(input().strip(), 0)
            table_rows.append(row)
        for row in table_rows:
            e1 = row[0]
            for i, e2 in enumerate(table_header[1:]):
                dist_mat[e1, e2] = float(row[i + 1])
        elem_types = table_header[1:]
        g = create_graph(g_as_list)
        leaf_nodes = {n for n in g.get_nodes() if g.get_degree(n) == 1}
        leaf_node = next(iter(leaf_nodes))
        seq_length = len(g.get_node_data(leaf_node)['seq'])
        print('The tree...')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
        print(f'... with {root} set as its root and the distances ...')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in elem_types:
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in elem_types:
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in elem_types:
                print(f'<td>{dist_mat[l1, l2]}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
        print(f'... has the following inferred ancestor sequences after using nearest neighbour interchange ...')
        def output_graph(_g, score):
            print()
            print(f'graph score: {score}')
            print()
            print(f'```{{dot}}')
            print(f'{to_dot(_g)}')
            print(f'```')
            print()
        input_score, output_score = nn_interchange(
            g,
            root,
            seq_length,
            lambda n: g.get_node_data(n)['seq'],
            lambda n, seq: g.get_node_data(n).update({'seq': seq}),
            lambda n, idx: g.get_node_data(n).get(f'dist_set_{idx}', {}),
            lambda n, idx, ds: g.get_node_data(n).update({f'dist_set_{idx}': ds}),
            lambda e1, e2: dist_mat[e1, e2],
            lambda e, score: g.get_edge_data(e).update({'score': score}),
            elem_types,
            output_graph
        )
        print(f'After applying the nearest neighbour interchange heuristic, the tree updated to have a parismony score'
              f' of {output_score} vs the original score of {input_score}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
    # g = Graph()
    # g.insert_node('1')
    # g.insert_node('2')
    # g.insert_node('7')
    # g.insert_node('8')
    # g.insert_node('9')
    # g.insert_node('A')
    # g.insert_node('B')
    # g.insert_edge('A1', 'A', '1')
    # g.insert_edge('A2', 'A', '2')
    # g.insert_edge('B7', 'B', '7')
    # g.insert_edge('B8', 'B', '8')
    # g.insert_edge('B9', 'B', '9')
    # g.insert_edge('AB', 'A', 'B')
    # swaps = nearest_neighbour_interchange_options(g, 'AB')
    # interchange_neighbours(g, 'AB', *swaps.pop())
    # for n1_side, n2_side in swaps:
    #     print(f'{set(n1_side)}  /  {set(n2_side)}')
    # # main()