from collections import Counter
from itertools import combinations
from typing import TypeVar

from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from helpers.Utils import slide_window

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')


def create_tree(edges: list[list[str, str]]) -> Graph:
    g = Graph()
    for n in {n for e in edges for n in e}:
        g.insert_node(n)
    for n1, n2 in edges:
        g.insert_edge(f'{n1}-{n2}', n1, n2)
    return g


def find_nodes_between_leaves(g: Graph, n: N, end_n: N, n_walk: list[N]):
    n_walk.append(n)
    if n == end_n:
        return True
    for e in g.get_outputs(n):
        n1, n2, _ = g.get_edge(e)
        if len(n_walk) >= 2 and {n1, n2} == {n_walk[-1], n_walk[-2]}:
            continue
        next_n = next(iter({n1, n2}.difference({n})))
        done = find_nodes_between_leaves(g, next_n, end_n, n_walk)
        if done:
            return True
    n_walk.pop()


class EdgeCounter:
    def __init__(self, tree: Graph[N, ND, E, float]):
        self.tree = tree
        self.leaf_nodes = [n for n in tree.get_nodes() if len(tuple(tree.get_outputs(n))) == 1]
        self.leaf_count = len(self.leaf_nodes)

    def path(self, n: N, end_n: N) -> list[E]:
        edges = []
        nodes = []
        find_nodes_between_leaves(self.tree, n, end_n, nodes)
        for (n1, n2), _ in slide_window(nodes, 2):
            found_edge = None
            for edge_id in self.tree.get_outputs(n1):
                _end1, _end2, _ed = self.tree.get_edge(edge_id)
                if n2 not in {_end1, _end2}:
                    continue
                if found_edge is not None:
                    raise ValueError(f'Multiple edges to same node not allowed: {n1, n2}')
                found_edge = edge_id
            if found_edge is None:
                raise ValueError(f'No edge found: {n1, n2}')
            edges.append(found_edge)
        return edges

    # MARKDOWN_COUNT
    def edge_count(self, l1: N) -> Counter[E]:
        # Collect paths from l1 to all other leaf nodes
        path_collection = []
        for l2 in self.leaf_nodes:
            if l1 == l2:
                continue
            path = self.path(l1, l2)
            path_collection.append(path)
        # Count edges across all paths
        edge_counts = Counter()
        for path in path_collection:
            edge_counts.update(path)
        # Return edge counts
        return edge_counts
    # MARKDOWN_COUNT

    # MARKDOWN_COMBINE_COUNT
    def combine_edge_count(self, l1: N, l2: N) -> Counter[E]:
        c1 = self.edge_count(l1)
        c2 = self.edge_count(l2)
        return c1 + c2
    # MARKDOWN_COMBINE_COUNT

    # MARKDOWN_NORMALIZED_COMBINE_COUNT
    def combine_edge_count_and_normalize(self, l1: N, l2: N) -> Counter[E]:
        edge_counts = self.combine_edge_count(l1, l2)
        path_edges = self.path(l1, l2)
        for e in path_edges:
            edge_counts[e] -= self.leaf_count - 2
        return edge_counts
    # MARKDOWN_NORMALIZED_COMBINE_COUNT

    # MARKDOWN_NEIGHBOUR_PATH_EDGE_COUNT_CHECK
    def neighbour_check(self, l1: N, l2: N) -> bool:
        path_edges = self.path(l1, l2)
        return len(path_edges) == 2
    # MARKDOWN_NEIGHBOUR_PATH_EDGE_COUNT_CHECK

    # MARKDOWN_REDUCE_TO_2_TEST
    def reduced_to_2_check(self, l1: N, l2: N) -> bool:
        p = self.path(l1, l2)
        c = self.combine_edge_count_and_normalize(l1, l2)
        return all(c[edge] == 2 for edge in p)  # if counts for all edges in p reduced to 2
    # MARKDOWN_REDUCE_TO_2_TEST

    # MARKDOWN_SEGREGATE_BY_EDGE
    def segregate_leaves(self, internal_edge: E) -> dict[N, N]:
        leaf_to_end = {}  # leaf -> one of the ends of internal_edge
        e1, e2 = self.tree.get_edge_ends(internal_edge)
        for l1 in self.leaf_nodes:
            # If path from l1 to e1 ends with internal_edge, it means that it had to
            # walk over the internal edge to get to e1, which ultimately means that l1
            # it isn't on the e1 side / it's on the e2 side. Otherwise, it's on the e1
            # side.
            p = self.path(l1, e1)
            if p[-1] != internal_edge:
                leaf_to_end[l1] = e1
            else:
                leaf_to_end[l1] = e2
        return leaf_to_end
    # MARKDOWN_SEGREGATE_BY_EDGE

    # MARKDOWN_NEIGHBOUR_DETECT
    def neighbour_detect(self) -> tuple[int, tuple[N, N]]:
        found_pair = None
        found_total_count = -1
        for l1, l2 in combinations(self.leaf_nodes, r=2):
            normalized_counts = self.combine_edge_count_and_normalize(l1, l2)
            total_count = sum(c for c in normalized_counts.values())
            if total_count > found_total_count:
                found_pair = l1, l2
                found_total_count = total_count
        return found_total_count, found_pair
    # MARKDOWN_NEIGHBOUR_DETECT

    def to_dot(self) -> str:
        ret = 'graph G {\n'
        ret += ' graph[rankdir=LR]\n'
        ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
        ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
        nodes = sorted(self.tree.get_nodes())
        for n in nodes:
            ret += f'{n}\n'
        for e in self.tree.get_edges():
            n1, n2 = self.tree.get_edge_ends(e)
            ret += f'{n1} -- {n2} [label=" "]\n'
        ret += '}'
        return ret

    def combine_count_and_normalize_all_to_dot_subgraph(self) -> str:
        ret = 'graph G {\n'
        ret += ' graph[rankdir=LR]\n'
        ret += ' node[shape = circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
        ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
        ret += ' ranksep=0.25\n'
        ret += ' fontname="Courier-Bold"\n'
        ret += ' fontsize=10\n'
        for l1, l2 in combinations(sorted(self.leaf_nodes), r=2):
            c = self.combine_edge_count_and_normalize(l1, l2)
            ret += f'  subgraph cluster_{l1}{l2} {{\n'
            ret += f'  label="combine_count_and_normalize({l1},{l2})"\n'
            nodes = self.tree.get_nodes()
            for n in nodes:
                ret += f'  {l1}{l2}_{n} [label="{n}"'
                if n == l1 or n == l2:
                    ret += ', style=filled, fillcolor=gray'
                ret += ']\n'
            for e in self.tree.get_edges():
                n1, n2 = self.tree.get_edge_ends(e)
                ret += f' {l1}{l2}_{n1} -- {l1}{l2}_{n2} [label=" ", penwidth="2.5", color="{":invis:".join(["black"] * c[e])}"]\n'
            ret += '}\n'
        ret += '}'
        return ret


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        edges, _ = str_to_list(input().strip(), 0)
        tree = create_tree(edges)
        cntr = EdgeCounter(tree)
        print('Given the tree...')
        print()
        print('```{dot}')
        print(f'{cntr.to_dot()}')
        print('```')
        print()
        count, (l1, l2) = cntr.neighbour_detect()
        print(f'neighbour_detect reported that {l1} and {l2} have the highest total edge count of {count} and as such '
              f'are guaranteed to be neighbours.')
        print()
        print('For each leaf pair in the tree, `combine_count_and_normalize()` totals are ... ')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in sorted(cntr.leaf_nodes):
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in sorted(cntr.leaf_nodes):
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in sorted(cntr.leaf_nodes):
                if l1 == l2:
                    res = 0
                else:
                    res = sum(cntr.combine_edge_count_and_normalize(l1, l2).values())
                print(f'<td>{res}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
        print('```{dot}')
        print(f'{cntr.combine_count_and_normalize_all_to_dot_subgraph()}')
        print('```')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
