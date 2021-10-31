from __future__ import annotations

import math
from collections import Counter

from graph import DirectedGraph



def to_dot(g: DirectedGraph.Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=TB]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n}\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -> {n2}\n'
    ret += '}'
    return ret




class NodeData:
    def __init__(self, element: str):
        self.element = element
        self.alphabet_scores = {ch: math.nan for ch in 'ACGT'}
        self.tagged = False

    def set_score(self, alphabet_elem: str, score: float):
        self.alphabet_scores[alphabet_elem] = score

    def get_score(self, alphabet_elem: str):
        return self.alphabet_scores[alphabet_elem]

    def resolve_element(self, p_element: str):
        # you can technically pick any minimum, but if you want to match the sample output you need to make it so that
        # it tries to tiebreak by looking at the parent's element (submitted here as p_element)
        min_score = min(self.alphabet_scores.values())
        possibilities = {k for k, v in self.alphabet_scores.items() if v == min_score}
        if p_element in possibilities:
            self.element = p_element
        else:
            self.element = possibilities.pop()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class EdgeData:
    def __init__(self):
        self.hamming_distance = math.inf

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


def alpha(symbol1: str, symbol2: str):
    if symbol1 == symbol2:
        return 0
    else:
        return 1


def compute_internal_node_score(tree: DirectedGraph.Graph[str, NodeData, str, EdgeData], n: str):
    n_ch1, n_ch2 = tuple(tree.get_edge_to(e) for e in tree.get_outputs(n))
    n_data = tree.get_node_data(n)
    n_ch1_data = tree.get_node_data(n_ch1)
    n_ch2_data = tree.get_node_data(n_ch2)
    for s in 'ACGT':
        ch1_min = min(n_ch1_data.get_score(_s) + alpha(s, _s) for _s in 'ACGT')
        ch2_min = min(n_ch2_data.get_score(_s) + alpha(s, _s) for _s in 'ACGT')
        n_data.set_score(s, ch1_min + ch2_min)


def small_parsimony(tree: DirectedGraph.Graph[str, NodeData, str, EdgeData]):
    for n in tree.get_nodes():
        n_data = tree.get_node_data(n)
        n_data.tagged = False
        if n.startswith('L'):  # is leaf node
            n_data.tagged = True
            for e in 'ACGT':
                if n_data.element == e:
                    n_data.set_score(e, 0.0)
                else:
                    n_data.set_score(e, math.inf)
    nodes_untagged_but_all_children_tagged = Counter()
    for n in tree.get_nodes():
        if n.startswith('L'):
            continue  # don't include leaf nodes
        nodes_untagged_but_all_children_tagged[n] = tree.get_out_degree(n)
        for e in tree.get_outputs(n):
            n_child = tree.get_edge_to(e)
            if tree.get_node_data(n_child).tagged:
                nodes_untagged_but_all_children_tagged[n] -= 1
    while len(nodes_untagged_but_all_children_tagged) > 0:
        ripe_nodes = [n for n, c in nodes_untagged_but_all_children_tagged.items() if c == 0]
        n = ripe_nodes.pop()
        n_data = tree.get_node_data(n)
        n_data.tagged = True
        compute_internal_node_score(tree, n)
        del nodes_untagged_but_all_children_tagged[n]
        for e in tree.get_inputs(n):
            p = tree.get_edge_from(e)
            nodes_untagged_but_all_children_tagged[p] -= 1


def backtrack_to_create_elements_and_weights(tree: DirectedGraph.Graph[str, NodeData, str, EdgeData]):
    root_n = [n for n in tree.get_nodes() if tree.get_in_degree(n) == 0].pop()
    root_n_data = tree.get_node_data(root_n)
    root_n_data.resolve_element('')
    pending = [root_n]
    while pending:
        n = pending.pop()
        for e in tree.get_outputs(n):
            n_from, n_to, e_data = tree.get_edge(e)
            n_from_data = tree.get_node_data(n_from)
            n_to_data = tree.get_node_data(n_to)
            n_to_data.resolve_element(n_from_data.element)
            elem_from = tree.get_node_data(n).element
            elem_to = tree.get_node_data(n_to).element
            e_data.hamming_distance = 0 if elem_from == elem_to else 1
            pending.append(n_to)


with open('/home/user/Downloads/dataset_240342_12.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = [s.strip() for s in data.strip().split('\n')]
seq_len_set = set()
for l in lines[1:]:
    src, dst = tuple(l.split('->'))
    if not src.isdigit():
        seq_len_set.add(len(src))
    if not dst.isdigit():
        seq_len_set.add(len(dst))
assert len(seq_len_set) == 1
seq_len = next(iter(seq_len_set))

g_per_idx = []
for i in range(seq_len):
    g: DirectedGraph.Graph[str, NodeData, str, EdgeData] = DirectedGraph.Graph()
    leaf_cnter = 0
    processed = set()
    for l in lines[1:]:
        src, dst = tuple(l.split('->'))
        if tuple(sorted([src, dst])) in processed:
            continue
        processed.add(tuple(sorted([src, dst])))
        # src add
        if src.isdigit():
            from_id = src
            from_elem = '?'
        else:
            from_id = f'L{leaf_cnter}'
            leaf_cnter += 1
            from_elem = src[i]
        if not g.has_node(from_id):
            g.insert_node(from_id, NodeData(from_elem))
        # dst add
        if dst.isdigit():
            to_id = dst
            to_elem = '?'
        else:
            to_id = f'L{leaf_cnter}'
            leaf_cnter += 1
            to_elem = dst[i]
        if not g.has_node(to_id):
            g.insert_node(to_id, NodeData(to_elem))
        # edge add
        e_id = f'{sorted([from_id, to_id])}'
        if not g.has_edge(e_id):
            g.insert_edge(e_id, from_id, to_id, EdgeData())
    g_per_idx.append(g)

# print(f'{to_dot(g_per_idx[0])}')

# WHAT IS THIS DOING?
#
# The problem is exactly the same as the other small parsimony problem. The only difference is that it's feeding you
# an undirected graph and you have to pick some edge to break and inject a root into to make it a directed graph. The
# algorithm is exactly the same, you're just turning the graph directed by injecting a root at some edge.
#
# Why then do we construct a DirectedGraph.Graph from the input? laziness. I could have just as well used
# UndirectedGraph.Graph and worked around the issues of not including duplicates (above when reading in the graph) and
# flipping edges around (below when injecting the root).
break_e_id = next(g_per_idx[0].get_edges())
break_from, break_to, break_data = g_per_idx[0].get_edge(break_e_id)
root_id = 'ROOT'
root_elem = '?'
for i in range(seq_len):
    g_per_idx[i].insert_node(root_id, NodeData(root_elem))
    g_per_idx[i].insert_edge('ROOT_A', root_id, break_from, EdgeData())
    g_per_idx[i].insert_edge('ROOT_B', root_id, break_to, EdgeData())
    g_per_idx[i].delete_edge(break_e_id)
    # ensure all edges are pointing away from ROOT
    pending = [(None, root_id)]
    while pending:
        parent_n, n = pending.pop()
        for e in set(g_per_idx[i].get_inputs(n)):
            n_from, n_to, e_data = g_per_idx[i].get_edge(e)
            if n_from != parent_n:
                # reverse edge
                g_per_idx[i].delete_edge(e)
                g_per_idx[i].insert_edge(e, n_to, n_from, e_data)
        for e in g_per_idx[i].get_outputs(n):
            n_to = g_per_idx[i].get_edge_to(e)
            pending.append((n, n_to))
# print(f'{to_dot(g_per_idx[0])}')

for i in range(seq_len):
    small_parsimony(g_per_idx[i])
    backtrack_to_create_elements_and_weights(g_per_idx[i])

# Remove the root, making sure to sum the hamming dist of its edges when merging it back into a single edge
for i in range(seq_len):
    new_hd = g_per_idx[i].get_edge_data('ROOT_A').hamming_distance + g_per_idx[i].get_edge_data('ROOT_B').hamming_distance
    new_ed = EdgeData()
    new_ed.hamming_distance = new_hd
    g_per_idx[i].insert_edge(break_e_id, break_from, break_to, new_ed)
    g_per_idx[i].delete_edge('ROOT_A')
    g_per_idx[i].delete_edge('ROOT_B')
    g_per_idx[i].delete_node('ROOT')
# print(f'{to_dot(g_per_idx[0])}')

min_parsimony_score = 0
for e in g_per_idx[0].get_edges():
    for i in range(seq_len):
        min_parsimony_score += g_per_idx[i].get_edge_data(e).hamming_distance
print(f'{min_parsimony_score}')

for e in g_per_idx[0].get_edges():
    n_from, n_to, _ = g_per_idx[0].get_edge(e)
    seq_from = ''.join(g.get_node_data(n_from).element for g in g_per_idx)
    seq_to = ''.join(g.get_node_data(n_to).element for g in g_per_idx)
    dist = sum(g.get_edge_data(e).hamming_distance for g in g_per_idx)
    print(f'{seq_from}->{seq_to}:{int(dist)}')
    print(f'{seq_to}->{seq_from}:{int(dist)}')

# print(g_per_idx)