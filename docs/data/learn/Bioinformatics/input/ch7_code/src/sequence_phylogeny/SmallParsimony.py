import math
from collections import Counter
from typing import TypeVar, Callable, Any, Optional, Iterable

from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list

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


def hamming_distance(e1: str, e2: str):
    if e1 == e2:
        return 0
    else:
        return 1


# MARKDOWN_POPULATE
def populate_distance_sets(
        tree: Graph[N, ND, E, ED],
        root: N,
        seq_length: int,
        get_sequence: Callable[[N], str],
        set_sequence: Callable[[N, str], None],
        get_dist_set: Callable[
            [
                N,   # node
                int  # index within N's sequence
            ],
            dict[str, float]
        ],
        set_dist_set: Callable[
            [
                N,    # node
                int,  # index within N's sequence
                dict[str, float]
            ],
            None
        ],
        dist_metric: Callable[[str, str], float],
        elem_types: str = 'ACTG'
) -> None:
    neighbours_unprocessed = Counter()
    for n in tree.get_nodes():
        neighbours_unprocessed[n] = tree.get_degree(n)
    leaf_nodes = {n for n, c in neighbours_unprocessed.items() if c == 1}
    internal_nodes = {n for n, c in neighbours_unprocessed.items() if c > 1}

    # Add +1 to the unprocessed count of the node deemed to be root. This
    # will make it so that it gets processed last.
    assert root in neighbours_unprocessed
    neighbours_unprocessed[root] += 1

    # Build dist sets for leaf nodes
    for n in leaf_nodes:
        # Build and set dist set for each element
        seq = get_sequence(n)
        for idx, elem in enumerate(seq):
            dist_set = distance_for_leaf_element_types(elem, elem_types)
            set_dist_set(n, idx, dist_set)
        # Decrement waiting count for upstream neighbour
        for edge in tree.get_outputs(n):
            n_upstream = tree.get_edge_end(edge, n)
            neighbours_unprocessed[n_upstream] -= 1
        # Remove from pending nodes
        neighbours_unprocessed.pop(n)

    # Build dist sets for internal nodes (walking up from leaf nodes)
    while True:
        # Get next node ready to be processed
        ready = {n for n, c in neighbours_unprocessed.items() if c == 1}
        if not ready:
            break
        n = ready.pop()
        # For each index, pull distance sets for outputs of n (that have them) and
        # use them to build a distance set for n.
        for i in range(seq_length):
            downstream_dist_sets = []
            for edge in tree.get_outputs(n):
                n_downstream = tree.get_edge_end(edge, n)
                # If it's root, treat all edges as pointing to downstream nodes
                # If it's not root, only nodes already processed are downstream nodes
                if n != root and n_downstream in neighbours_unprocessed:
                    continue  # Skip -- not root + not processed = actually upstream node
                dist_set = get_dist_set(n_downstream, i)
                downstream_dist_sets.append(dist_set)
            dist_set = distance_for_internal_element_types(
                downstream_dist_sets,
                dist_metric,
                elem_types
            )
            set_dist_set(n, i, dist_set)
        # Mark neighbours as processed
        for edge in tree.get_outputs(n):
            n_upstream = tree.get_edge_end(edge, n)
            if n_upstream in neighbours_unprocessed:
                neighbours_unprocessed[n_upstream] -= 1
        # Remove from pending nodes
        neighbours_unprocessed.pop(n)

    # Set sequences for internal nodes based on dist sets
    for n in internal_nodes:
        seq = ''
        for i in range(seq_length):
            elem, _ = min(
                ((elem, dist) for elem, dist in get_dist_set(n, i).items()),
                key=lambda x: x[1]  # sort on dist
            )
            seq += elem
        set_sequence(n, seq)
# MARKDOWN_POPULATE


# MARKDOWN_INTERNAL_DIST_SET
def distance_for_internal_element_types(
        downstream_dist_sets: Iterable[dict[str, float]],
        dist_metric: Callable[[str, str], float],
        elem_types: str = 'ACTG'
) -> dict[str, float]:
    dist_set = {}
    for elem_type in elem_types:
        dist = distance_for_internal_element_type(
            downstream_dist_sets,
            dist_metric,
            elem_type,
            elem_types
        )
        dist_set[elem_type] = dist
    return dist_set


def distance_for_internal_element_type(
        downstream_dist_sets: Iterable[dict[str, float]],
        dist_metric: Callable[[str, str], float],
        elem_type_dst: str,
        elem_types: str = 'ACTG'
) -> float:
    min_dists = []
    for downstream_dist_set in downstream_dist_sets:
        possible_dists = []
        for elem_type_src in elem_types:
            downstream_dist = downstream_dist_set[elem_type_src]
            transition_cost = dist_metric(elem_type_src, elem_type_dst)
            dist = downstream_dist + transition_cost
            possible_dists.append(dist)
        min_dist = min(possible_dists)
        min_dists.append(min_dist)
    return sum(min_dists)
# MARKDOWN_INTERNAL_DIST_SET


# MARKDOWN_LEAF_DIST_SET
def distance_for_leaf_element_types(
        elem_type_dst: str,
        elem_types: str = 'ACTG'
) -> dict[str, float]:
    dist_set = {}
    for e in elem_types:
        if e == elem_type_dst:
            dist_set[e] = 0.0
        else:
            dist_set[e] = math.inf
    return dist_set
# MARKDOWN_LEAF_DIST_SET


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
        print(f'... with {root} set as its root ...')
        print()
        print(f'... and the distances ...')
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
        print(f'... has the following inferred ancestor sequences ...')
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