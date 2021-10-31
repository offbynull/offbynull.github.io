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


for p in options:
    print(f'{p}')


def nearest_neighbours(t: UndirectedGraph.Graph, edge_id):
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
    return t1, t2


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
    pending = [(0, t1)]
    while pending:
        cnt, t = pending.pop()
        if is_equal(t, t2):
            return cnt
        t_options = []
        t_options += nearest_neighbours(t, 'AB')
        t_options += nearest_neighbours(t, 'BC')
        t_options_walked_removed = []
        for t_new in t_options:
            if all(not is_equal(t_new, t_walked) for _, t_walked in walked):
                t_options_walked_removed.append(t_new)
        for t_new in t_options_walked_removed:
            if all(not is_equal(t_new, t_pending) for _, t_pending in pending):
                pending.append((cnt+1, t_new))
        walked.append(t)


max_steps = 0
for t1, t2 in product(tree_list, repeat=2):
    steps = find_steps(t1, t2)
    if steps > max_steps:
        steps = max_steps


THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT
THIS CODE IS BUGGED FIX IT

print(f'{max_steps}')