from typing import List, Tuple

from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240327_8(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
line = lines[0]
edge_list = [s for s in line[1:-1].split('), (')]
edge_list = [x.split(', ') for x in edge_list]
edge_list = [(int(x1), int(x2)) for x1, x2 in edge_list]


def cycle_to_chromosome(c: List[int]) -> List[int]:
    chromosome_offset = min(c) // 2 + 1
    p = []
    p_size = len(c) // 2
    for x1, x2, idx in zip(c[::2], c[1::2], range(0, p_size)):
        if x1 < x2:
            p.append(chromosome_offset + idx)
        else:
            p.append(-(chromosome_offset + idx))
    return p


def graph_to_genome(edges: List[Tuple[int, int]]) -> List[List[int]]:
    p_list = []
    cycles = []
    cycle_start_idx = -1
    cycle_end_idx = -1
    for i, p in enumerate(edges):
        if cycle_start_idx == -1:
            cycle_start_idx = i
        elif (p[1] == edges[cycle_start_idx][0] + 1 or p[1] == edges[cycle_start_idx][0] - 1) and cycle_end_idx == -1:
            cycle_end_idx = i
            cycles += [edges[cycle_start_idx:cycle_end_idx+1]]
            cycle_start_idx = -1
            cycle_end_idx = -1
    for c in cycles:
        nodes = [n for e in c for n in e]
        adjusted_nodes = nodes[-1:] + nodes[0:-1]
        adjusted_chromosome = cycle_to_chromosome(adjusted_nodes)
        p_list += [adjusted_chromosome]
    return p_list


x = ''
for p_list in graph_to_genome(edge_list):
    x += '('
    x += ' '.join([('+' if p > 0 else '') + str(p) for p in p_list])
    x += ')'
print(f'{x}')
