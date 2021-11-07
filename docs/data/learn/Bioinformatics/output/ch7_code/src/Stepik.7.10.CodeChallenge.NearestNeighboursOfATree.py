from __future__ import annotations

import math
from collections import Counter

from graph import DirectedGraph, UndirectedGraph


def to_dot(g_list: list[UndirectedGraph.Graph]) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    ret += ' layout=dot\n'
    for i, g in enumerate(reversed(g_list)):
        ret += f' subgraph cluster_{i} {{\n'
        if i == len(g_list) - 1:
            ret += f'   label=orig\n'
        else:
            ret += f'   label=nn{i+1}\n'
        nodes = sorted(g.get_nodes())
        for n in nodes:
            ret += f'  x{n}x{i} [label={n}]\n'
        for e in sorted(g.get_edges()):
            n1, n2, weight = g.get_edge(e)
            ret += f'  x{n1}x{i} -- x{n2}x{i}\n'
        ret += ' }\n'
    ret += '}'
    return ret


def nn_swap(edge_id: str, t: UndirectedGraph.Graph):
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


with open('/home/user/Downloads/dataset_240343_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = [s.strip() for s in data.strip().split('\n')]
n1, n2 = sorted(lines[0].split())
swap_e = f'{n1, n2}'
t = UndirectedGraph.Graph()
for l in lines[1:]:
    src, dst = sorted(l.split('->'))
    e = f'{src, dst}'
    if t.has_edge(e):
        continue
    if not t.has_node(src):
        t.insert_node(src)
    if not t.has_node(dst):
        t.insert_node(dst)
    t.insert_edge(e, src, dst)

t1, t2 = nn_swap(swap_e, t)

for e in t1.get_edges():
    n1, n2 = t1.get_edge_ends(e)
    print(f'{n1}->{n2}')
    print(f'{n2}->{n1}')
print()
for e in t2.get_edges():
    n1, n2 = t2.get_edge_ends(e)
    print(f'{n1}->{n2}')
    print(f'{n2}->{n1}')


# print(to_dot([t, t1, t2]))