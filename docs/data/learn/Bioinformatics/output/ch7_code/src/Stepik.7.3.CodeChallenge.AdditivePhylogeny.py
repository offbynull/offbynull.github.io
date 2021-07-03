import re
from itertools import product

from graph import UndirectedGraph
from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240336_11.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = [s.strip() for s in data.strip().split('\n')]
mat_size = int(lines[0])
dist_mat = [[int(e) for e in row.split()] for row in lines[1:]]


def calc_limb_length(d: [[int]], leaf_idx: int):
    d_len = len(d)
    min_limb_len = None
    for i, k in product(range(d_len), range(d_len)):
        if i == leaf_idx or k == leaf_idx:
            continue
        limb_len = (d[i][leaf_idx] + d[k][leaf_idx] - d[i][k]) // 2
        if min_limb_len is None or limb_len < min_limb_len:
            min_limb_len = limb_len
    return min_limb_len


def to_bald_matrix(d: [[int]], limb_len: int) -> [[int]]:
    d = [r[:] for r in d]
    n = len(d)
    for i in range(n - 1):
        d[n - 1][i] -= limb_len
        d[i][n - 1] -= limb_len
    return d


def to_trimmed_matrix(d: [[int]]) -> [[int]]:
    return [r[:-1] for r in d[:-1]]


def find_additive_distance(d: [[int]]) -> (int, int):
    n = len(d) - 1
    for i, k in product(range(n), range(n)):
        if i == k:
            continue
        if d[i][k] == d[i][n] + d[n][k]:
            return i, k
    raise ValueError('???')


class WrappedInt:
    def __init__(self, start=0):
        self.i = start

    def next(self):
        ret = self.i
        self.i += 1
        return ret


def additive_phylogeny(d: [[int]], counter: WrappedInt):
    if len(d) == 2:
        g = UndirectedGraph.Graph()
        g.insert_node('0')
        g.insert_node('1')
        g.insert_edge('0-1', '0', '1', d[0][1])
        return g, '0-1', d[0][1]
    n = len(d) - 1
    limb_len = calc_limb_length(d, n)
    bald_d = to_bald_matrix(d, limb_len)
    i, k = find_additive_distance(bald_d)
    x = bald_d[i][n]
    trimmed_d = to_trimmed_matrix(bald_d)
    t, last_added_edge, weight_from_i = additive_phylogeny(trimmed_d, counter)
    v = f'{counter.next()}'
    t.insert_node(v)
    orig_edge_weight = t.get_edge_data(last_added_edge)
    orig_edge_start, orig_edge_end = t.get_edge_ends(last_added_edge)
    t.delete_edge(last_added_edge)
    t.insert_edge(f'{orig_edge_start}-{v}', f'{orig_edge_start}', v, orig_edge_weight - (weight_from_i - x))
    t.insert_edge(f'{v}-{orig_edge_end}', v, f'{orig_edge_end}', weight_from_i - x)
    t.insert_node(f'{n}')
    t.insert_edge(f'{v}-{n}', v, f'{n}', limb_len)
    return t, f'{v}-{n}', x + limb_len


if __name__ == '__main__':
    d = [
        [0, 13, 21, 22],
        [13, 0, 12, 13],
        [21, 12, 0, 13],
        [22, 13, 13, 0]
    ]
    graph, _, _ = additive_phylogeny(d, WrappedInt(len(d)))
    output = []
    for e in graph.get_edges():
        n1, n2 = graph.get_edge_ends(e)
        weight = graph.get_edge_data(e)
        output.append(f'{n1}->{n2}: {weight}')
        output.append(f'{n2}->{n1}: {weight}')
    output.sort()
    print('\n'.join(output))