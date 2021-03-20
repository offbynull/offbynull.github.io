from typing import List, Tuple

from helpers.Utils import slide_window

with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
p_list1 = [[int(x) for x in s.split(' ')] for s in lines[0][1:-1].split(')(')]
p_list2 = [[int(x) for x in s.split(' ')] for s in lines[1][1:-1].split(')(')]


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


def count_synteny_blocks(p_list: List[List[int]]) -> int:
    blocks = 0
    for p in p_list:
        blocks += len(p)
    return blocks


def count_cycles(edges: List[Tuple[int, int]]) -> int:
    cycles = 0
    cycle_start_idx = -1
    for i, p in enumerate(edges):
        if cycle_start_idx == -1:
            cycle_start_idx = i
        elif p[1] == edges[cycle_start_idx][0] + 1 or p[1] == edges[cycle_start_idx][0] - 1:
            cycles += 1
            cycle_start_idx = -1
    assert cycle_start_idx == -1
    return cycles


DOESNT WORK MAKE AST AND TRY AGAIN
DOESNT WORK MAKE AST AND TRY AGAIN
DOESNT WORK MAKE AST AND TRY AGAIN
DOESNT WORK MAKE AST AND TRY AGAIN
DOESNT WORK MAKE AST AND TRY AGAIN
DOESNT WORK MAKE AST AND TRY AGAIN


print(f'{colored_edges(p_list1)}')
print(f'{colored_edges(p_list2)}')

merged_colored_edges = colored_edges(p_list1) + colored_edges(p_list2)
print(f'{merged_colored_edges}')

print(f'{count_synteny_blocks(p_list1)}')
print(f'{count_cycles(colored_edges(p_list1))}')
print(f'{count_cycles(colored_edges(p_list2))}')
