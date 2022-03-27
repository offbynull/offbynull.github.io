# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION
# THIS IS WRONG. SEE STEPTIK 9.21 CODE CHALLENGE FOR CORRECT IMPLEMENTATION

from __future__ import annotations

import functools

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
        ret += f'{n1} -> {n2} [label="{data}"]\n'
    ret += '}'
    return ret


def cmp(a: str, b: str):
    for a_ch, b_ch in zip(a, b):
        if a_ch == '$' and b_ch == '$':
            continue
        if a_ch == '$':
            return -1
        if b_ch == '$':
            return 1
        if a_ch < b_ch:
            return -1
        if a_ch > b_ch:
            return 1
    if len(a) < len(b):
        return a
    elif len(b) < len(a):
        return b
    raise '???'


def construct_suffix_array(text: str):
    ret = []
    for i in range(len(text) - 1, -1, -1):
        region = text[i:]
        ret.append(region)
    ret = sorted(ret, key=functools.cmp_to_key(cmp))
    return ret


def longest_common_prefix(s1: str, s2: str):
    ret = 0
    for ch1, ch2 in zip(s1, s2):
        if ch1 == ch2:
            ret += 1
        else:
            return ret
    return ret


def construct_lcp_array_from_suffix_array(suff_arr: list[str]):
    ret = [0]
    for (s1, s2), _ in slide_window(suff_arr, 2):
        ret.append(longest_common_prefix(s1, s2))
    return ret


def to_suffix_tree(suffix_array: list[str], lcp_array: list[int]) -> Graph[int, None, int, str]:
    tree = Graph()
    tree.insert_node(0)
    e_gen = IntegerIdGenerator(start_count=10000)
    n_gen = IntegerIdGenerator(start_count=1)
    n_chain = [0]
    last_lcp = lcp_array[0]
    lcp_array = lcp_array + [0]  # add phony element at the end -- not required for anything but it prevents off by one crash when processing last element of suffix array
    for i, segment in enumerate(suffix_array):
        lcp = lcp_array[i+1]
        if lcp > last_lcp:
            # insert shared part as intenal edge
            n = n_chain[-1]
            n_new = n_gen.next_id()
            e_new = e_gen.next_id()
            tree.insert_node(n_new)
            tree.insert_edge(e_new, n, n_new, segment[last_lcp:lcp])
            n_chain.append(n_new)  # add to chain
            n = n_new
            # insert remainder part as limb
            n_new = n_gen.next_id()
            e_new = e_gen.next_id()
            tree.insert_node(n_new)
            tree.insert_edge(e_new, n, n_new, segment[lcp:])
        elif lcp < last_lcp:
            n = n_chain[-1]
            n_new = n_gen.next_id()
            e_new = e_gen.next_id()
            tree.insert_node(n_new)
            tree.insert_edge(e_new, n, n_new, segment[last_lcp:])
            n_chain.pop()
        else:
            n = n_chain[-1]
            n_new = n_gen.next_id()
            e_new = e_gen.next_id()
            tree.insert_node(n_new)
            tree.insert_edge(e_new, n, n_new, segment[last_lcp:])
        last_lcp = lcp
    return tree


text = 'panamabananas$'
suffix_array = construct_suffix_array(text)
lcp_array = construct_lcp_array_from_suffix_array(suffix_array)

tree = to_suffix_tree(suffix_array, lcp_array)
print(f'{to_dot(tree)}')