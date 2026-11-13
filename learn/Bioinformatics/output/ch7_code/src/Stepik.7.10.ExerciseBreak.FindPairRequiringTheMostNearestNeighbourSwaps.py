# Exercise Break: The figure below shows all possible unrooted binary trees with five leaves. Find a pair of these
# trees that are the “farthest apart” in that they require the maximum number of nearest neighbor interchanges to
# transform one tree into the other.
#
#    j   k
#    |   |
# i--*   *--l
#     \ /
#      *
#      |
#      m
#
# The above is repeated 15 times with different orderings of A B C D and E




# MY ANSWER IS BELOW. I ORIGINALL THOUGHT IT WAS 5 JUST BY LOOKING AT THE PROBLEM, BUT IT LOOKS LIKE THE ANSWER IS 7
# SWAPS ARE REQUIRED

from itertools import permutations, product

from graph import UndirectedGraph


options = set()
for c in permutations(['i', 'j', 'k', 'l', 'm'], r=5):
    pairing = set()
    pairing.add(frozenset(c[0:2]))
    pairing.add(frozenset(c[2:4]))
    pairing.add(frozenset(c[4]))
    options.add(frozenset(pairing))

tree_list = []
for option in options:
    t = UndirectedGraph.Graph()
    t.insert_node('i')
    t.insert_node('j')
    t.insert_node('k')
    t.insert_node('l')
    t.insert_node('m')
    t.insert_node('C')
    t.insert_node('B')
    t.insert_node('A')
    t.insert_edge('AB', 'A', 'B')
    t.insert_edge('BC', 'B', 'C')
    option = sorted((list(p) for p in option), key=lambda x: len(x))
    t.insert_edge('B0', 'B', option[0][0])
    t.insert_edge('A0', 'A', option[1][0])
    t.insert_edge('A1', 'A', option[1][1])
    t.insert_edge('C0', 'C', option[2][0])
    t.insert_edge('C1', 'C', option[2][1])
    tree_list.append(t)


# for p in options:
#     print(f'{p}')


def nearest_neighbours(t: UndirectedGraph.Graph):
    leaf_ids = {_n for _n in t.get_nodes() if t.get_degree(_n) == 1}
    internal_node_ids = {_n for _n in t.get_nodes() if _n not in leaf_ids}
    internal_edge_ids = {_e for _e in t.get_edges() if t.get_edge_ends(_e)[0] in internal_node_ids and t.get_edge_ends(_e)[1] in internal_node_ids}
    ret = []
    for edge_id in internal_edge_ids:
        n1, n2, _ = t.get_edge(edge_id)
        n1_edge_ids = [e for e in t.get_outputs(n1) if e != edge_id]
        n2_edge_ids = [e for e in t.get_outputs(n2) if e != edge_id]
        n1_1, n1_2 = [_n for e in n1_edge_ids for _n in t.get_edge_ends(e) if _n != n1]
        n2_1, n2_2 = [_n for e in n2_edge_ids for _n in t.get_edge_ends(e) if _n != n2]
        t1 = t.copy()
        t1.delete_edge(n1_edge_ids[0])
        t1.delete_edge(n1_edge_ids[1])
        t1.delete_edge(n2_edge_ids[0])
        t1.delete_edge(n2_edge_ids[1])
        t1.insert_edge(n1_edge_ids[0], n1, n1_1)
        t1.insert_edge(n1_edge_ids[1], n1, n2_1)
        t1.insert_edge(n2_edge_ids[0], n2, n1_2)
        t1.insert_edge(n2_edge_ids[1], n2, n2_2)
        t2 = t.copy()
        t2.delete_edge(n1_edge_ids[0])
        t2.delete_edge(n1_edge_ids[1])
        t2.delete_edge(n2_edge_ids[0])
        t2.delete_edge(n2_edge_ids[1])
        t2.insert_edge(n1_edge_ids[0], n1, n1_1)
        t2.insert_edge(n1_edge_ids[1], n1, n2_2)
        t2.insert_edge(n2_edge_ids[0], n2, n1_2)
        t2.insert_edge(n2_edge_ids[1], n2, n2_1)
        ret += (t1, t2)
    return ret


def is_equal(t1: UndirectedGraph.Graph, t2: UndirectedGraph.Graph):
    t1_A_nodes = frozenset(_n for e in t1.get_outputs('A') for _n in t1.get_edge_ends(e) if not _n.isupper())
    t1_B_nodes = frozenset(_n for e in t1.get_outputs('B') for _n in t1.get_edge_ends(e) if not _n.isupper())
    t1_C_nodes = frozenset(_n for e in t1.get_outputs('C') for _n in t1.get_edge_ends(e) if not _n.isupper())
    t2_A_nodes = frozenset(_n for e in t2.get_outputs('A') for _n in t2.get_edge_ends(e) if not _n.isupper())
    t2_B_nodes = frozenset(_n for e in t2.get_outputs('B') for _n in t2.get_edge_ends(e) if not _n.isupper())
    t2_C_nodes = frozenset(_n for e in t2.get_outputs('C') for _n in t2.get_edge_ends(e) if not _n.isupper())
    return frozenset([t1_A_nodes, t1_B_nodes, t1_C_nodes]) == frozenset([t2_A_nodes, t2_B_nodes, t2_C_nodes])


def find_steps(t1: UndirectedGraph.Graph, t2: UndirectedGraph.Graph):
    walked = []
    pending = [([t1], t1)]
    while pending:
        t_steps, t = pending.pop()
        walked.append(t)
        if is_equal(t, t2):
            return t_steps
        t_options = nearest_neighbours(t)
        # remove if already walked
        t_options_not_already_walked = []
        for t_option in t_options:
            if all(not is_equal(t_option, t_walked) for t_walked in walked):
                t_options_not_already_walked.append(t_option)
        # remove if already pending
        t_options_not_already_walked_or_pending = []
        for t_option in t_options_not_already_walked:
            if all(not is_equal(t_option, t_pending) for _, t_pending in pending):
                t_options_not_already_walked_or_pending.append(t_option)
        # put remaining in pending
        for t_option in t_options_not_already_walked_or_pending:
            pending.append((t_steps + [t_option], t_option))


def main():
    max_steps = []
    for t1, t2 in product(tree_list, repeat=2):
        steps = find_steps(t1, t2)
        if len(steps) > len(max_steps):
            max_steps = steps
    print(f'{to_dot(max_steps)}')


def to_dot(g_list: list[UndirectedGraph.Graph]) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    ret += ' layout=dot\n'
    for i, g in enumerate(g_list):
        ret += f' subgraph cluster_{i} {{\n'
        if i == 0:
            ret += f'   label=start\n'
        elif i == len(g_list) - 1:
            ret += f'   label="swap{i} (end)"\n'
        else:
            ret += f'   label=swap{i}\n'
        nodes = sorted(g.get_nodes())
        for n in nodes:
            ret += f'  {n}_{i} [label={n}]\n'
        for e in sorted(g.get_edges()):
            n1, n2, weight = g.get_edge(e)
            ret += f'  {n1}_{i} -- {n2}_{i}\n'
        ret += ' }\n'
    ret += '}'
    return ret


if __name__ == '__main__':
    main()