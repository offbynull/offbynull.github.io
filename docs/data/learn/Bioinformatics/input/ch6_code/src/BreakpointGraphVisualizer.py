from math import pi, cos, sin
from typing import List

from helpers.Utils import slide_window


def generate_graph(src: List[List[int]], dst: List[List[int]]):
    g = ''
    g += 'graph G {\n'
    g += 'node [shape=plain];\n'

    node_count = sum(len(p) for p in src) * 2
    radius = node_count ** 1/4
    node_locations = [(cos(2 * pi / node_count * x) * radius, sin(2 * pi / node_count * x) * radius) for x in range(0, node_count + 1)]

    for p in src:
        for s in p:
            x1, y1 = node_locations.pop()
            x2, y2 = node_locations.pop()
            if s > 0:
                g += f'_{s}h_ [pos="{x1},{y1}!"];\n'
                g += f'_{s}t_ [pos="{x2},{y2}!"];\n'
            elif s < 0:
                g += f'_{-s}t_ [pos="{x1},{y1}!"];\n'
                g += f'_{-s}h_ [pos="{x2},{y2}!"];\n'

    # Draw black edges
    for p in src:
        for s in p:
            if s > 0:
                g += f'_{s}h_ -- _{s}t_ [style=dashed, dir=forward];\n'
            elif s < 0:
                g += f'_{-s}t_ -- _{-s}h_ [style=dashed, dir=back];\n'
            else:
                raise ValueError('???')

    # Draw blue edges (source)
    for p in src:
        for (s1, s2), idx in slide_window(p, 2, cyclic=True):
            if s1 < 0 and s2 > 0:
                g += f'_{-s1}h_ -- _{s2}h_ [color=blue];\n'
            elif s1 > 0 and s2 < 0:
                g += f'_{s1}t_ -- _{-s2}t_ [color=blue];\n'
            elif s1 > 0 and s2 > 0:
                g += f'_{s1}t_ -- _{s2}h_ [color=blue];\n'
            elif s1 < 0 and s2 < 0:
                g += f'_{-s1}h_ -- _{-s2}t_ [color=blue];\n'
            else:
                raise ValueError('???')

    # Draw red edges (destination)
    for p in dst:
        for (s1, s2), idx in slide_window(p, 2, cyclic=True):
            if s1 < 0 and s2 > 0:
                g += f'_{-s1}h_ -- _{s2}h_ [color=red];\n'
            elif s1 > 0 and s2 < 0:
                g += f'_{s1}t_ -- _{-s2}t_ [color=red];\n'
            elif s1 > 0 and s2 > 0:
                g += f'_{s1}t_ -- _{s2}h_ [color=red];\n'
            elif s1 < 0 and s2 < 0:
                g += f'_{-s1}h_ -- _{-s2}t_ [color=red];\n'
            else:
                raise ValueError('???')

    g += '}'

    return g


# print(f'{generate_graph([[+1, -2, -3, +4]], [[+1, +2, -4, -3]])}')
# print(f'{generate_graph([[+1, -2, -3, +4, +5, +6]], [[+1, +2, -4, -3, +5, +6]])}')
# print(f'{generate_graph([[+9, -8, +12, +7, +1, -14, +13, +3, -5, -11, +6, -2, +10, -4]], [[-11, +8, -10, -2, +3, +4, +13, +6, +12, +9, +5, +7, -14, -1]])}')
# print(f'{generate_graph([[+9, -8, +12, +7, +1, -14, +13, +3, -5, -11, +6, -2, +10, -4]], [[+9, -8, +12], [+13, +3, +4, -10, +2, -6, +11, +1, +14], [+5, +7]])}')
print(f'{generate_graph([[+9, -8, +12], [+13, +3, +4, -10, +2, -6, +11, +1, +14], [+5, +7]], [[+9, -8, +12, +7, +1, -14, +13, +3, -5, -11, +6, -2, +10, -4]])}')
