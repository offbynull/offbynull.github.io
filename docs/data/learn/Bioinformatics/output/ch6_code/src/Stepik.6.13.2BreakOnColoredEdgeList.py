from typing import List, Tuple

from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240328_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
edge_list = [s for s in lines[0][1:-1].split('), (')]
edge_list = [x.split(', ') for x in edge_list]
edge_list = [(int(x1), int(x2)) for x1, x2 in edge_list]
_2break = lines[1].split(', ')
_2break = (int(_2break[0]), int(_2break[1]), int(_2break[2]), int(_2break[3]))


def perform_2_break(edges: List[Tuple[int, int]], _2break: Tuple[int, int, int, int]):
    if (_2break[0], _2break[1]) in edges:
        idx = edges.index((_2break[0], _2break[1]))
        edges[idx] = (_2break[0], _2break[2])
    elif (_2break[1], _2break[0]) in edges:
        idx = edges.index((_2break[1], _2break[0]))
        edges[idx] = (_2break[2], _2break[0])

    if (_2break[2], _2break[3]) in edges:
        idx = edges.index((_2break[2], _2break[3]))
        edges[idx] = (_2break[1], _2break[3])
    elif (_2break[3], _2break[2]) in edges:
        idx = edges.index((_2break[3], _2break[2]))
        edges[idx] = (_2break[3], _2break[1])


perform_2_break(edge_list, _2break)
print(f'{", ".join([str(x) for x in edge_list])}')