from typing import List, Tuple

from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240327_7.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
line = lines[0]
p_list = [[int(x) for x in s.split(' ')] for s in line[1:-1].split(')(')]


def chromosome_to_cycle(p: List[int]) -> List[int]:
    ret = []
    for i, chromosome in enumerate(p):
        i += 1
        if chromosome > 0:
            ret.append(2*i - 1)
            ret.append(2*i)
        else:
            ret.append(2*i)
            ret.append(2*i - 1)
    return ret


def colored_edges(p_list: List[List[int]]) -> List[Tuple[int, int]]:
    edges = []
    offset = 0
    for p in p_list:
        nodes = chromosome_to_cycle(p)
        nodes = [n + offset for n in nodes]  # add offset to chromosome's node ids
        offset += len(nodes)        # update offset used to shift next chromosome's node ids
        nodes = nodes + nodes[0:2]  # loop around to last 2 elements to simulate a cycle
        for x1, x2 in zip(nodes[1::2], nodes[2::2]):
            edges.append((x1, x2))
    return edges


print(f'{", ".join([str(x) for x in colored_edges(p_list)])}')
