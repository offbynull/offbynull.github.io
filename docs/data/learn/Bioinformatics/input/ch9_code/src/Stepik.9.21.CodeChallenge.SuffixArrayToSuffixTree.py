from __future__ import annotations

import functools
from typing import Any

from graph.DirectedGraph import Graph
from graph.GraphHelpers import IntegerIdGenerator
from helpers.Utils import slide_window


def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' rankdir=LR\n'
    ret += ' node[fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        data = g.get_node_data(n)
        ret += f'{n} [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        ret += f'{n1} -> {n2} [label="{data.text}"]\n'
    ret += '}'
    return ret





class NodeData:
    def __init__(self, ch_len: int):
        self.ch_len = ch_len  # num of chars so far from root to this node -- called "descent" in the book

    def __str__(self):
        return f'{self.ch_len}'

    def __repr__(self):
        return str(self)


class EdgeData:
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return str(self)


def to_suffix_tree(suffix_array: list[str], lcp_array: list[int]) -> Graph[int, NodeData, int, EdgeData]:
    tree = Graph()
    tree.insert_node(0, NodeData(0))
    e_gen = IntegerIdGenerator(start_count=10000)
    n_gen = IntegerIdGenerator(start_count=1)
    n = 0
    assert len(suffix_array) == len(lcp_array)
    i = 0
    while i < len(suffix_array):
        lcp = lcp_array[i]
        suffix = suffix_array[i]
        parent_len = tree.get_node_data(n).ch_len
        if lcp > parent_len:
            shared_prefix = suffix[parent_len:lcp]
            e_cut, e_cut_text = [(e, ed.text) for e, _, _, ed in tree.get_outputs_full(n) if ed.text.startswith(shared_prefix)].pop()
            existing_remainder = e_cut_text[lcp - parent_len:]
            n_new = n_gen.next_id()
            e_new1 = e_gen.next_id()
            e_new2 = e_gen.next_id()
            tree.insert_node_between_edge(
                n_new, NodeData(lcp),
                e_cut,
                e_new1, EdgeData(shared_prefix),
                e_new2, EdgeData(existing_remainder)
            )
            n = n_new
            continue
        elif lcp < parent_len:
            _, n, _, _ = tree.get_input_full(n)
            continue
        else:
            suffix_len = len(suffix)
            e_text = suffix[parent_len:]
            n_new = n_gen.next_id()
            e_new = e_gen.next_id()
            tree.insert_node(n_new, NodeData(suffix_len))
            tree.insert_edge(e_new, n, n_new, EdgeData(e_text))
            i += 1
    return tree


with open('/home/user/Downloads/dataset_240394_8.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = [l.strip() for l in data.strip().split('\n')]
text = lines[0]
suffix_array = [text[int(idx):] for idx in lines[1].split()]
lcp_array = [int(lcp) for lcp in lines[2].split()]

tree = to_suffix_tree(suffix_array, lcp_array)
edge_strs = [tree.get_edge_data(e).text for e in tree.get_edges()]
print(' '.join(edge_strs))

# for suffix, lcp in zip(suffix_array, lcp_array):
#     print('|' * lcp)
#     print(suffix)
# print(f'{to_dot(tree)}')