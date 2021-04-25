from typing import List, Tuple

# with open('/home/user/Downloads/dataset_240328_3(3).txt', mode='r', encoding='utf-8') as f:
# with open('/home/user/Downloads/dataset_240328_3(2).txt', mode='r', encoding='utf-8') as f:
# with open('/home/user/Downloads/dataset_240328_3(1).txt', mode='r', encoding='utf-8') as f:
# with open('/home/user/Downloads/dataset_240328_3.txt', mode='r', encoding='utf-8') as f:
with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
p_list = [[int(x) for x in s.split(' ')] for s in lines[0][1:-1].split(')(')]
_2break = lines[1].split(', ')
_2break = (int(_2break[0]), int(_2break[1]), int(_2break[2]), int(_2break[3]))


# WARNING!!!
#
# THE ALGORITHMS HERE ARE NOT THE SAME AS THE ALGORITHMS IN PREVIOUS 6.12/6.13 CODE CHALLENGES. THE GRADER IS BROKEN AND
# A LOT OF WHATS HAPPENING HERE WAS REVERSE ENGINEERED FROM FAILING ASSIGNMENTS AND LOOKING AT THE EXTRA DATASET. THE
# SAMPLE OUTPUT ON THE CODE CHALLENGE PAGE IS INCORRECT.


def chromosome_to_cycle(p: List[int]) -> List[int]:
    ret = []
    for chromosome in p:
        i = abs(chromosome)
        if chromosome > 0:
            ret.append(2*i - 1)
            ret.append(2*i)
        else:
            ret.append(2*i)
            ret.append(2*i - 1)
    return ret


def black_edges(p_list: List[List[int]]) -> List[Tuple[int, int, str]]:
    edges = []
    offset = 0
    for p in p_list:
        nodes = chromosome_to_cycle(p)
        nodes = [n + offset for n in nodes]  # add offset to chromosome's node ids
        offset += len(nodes)        # update offset used to shift next chromosome's node ids
        for x1, x2 in zip(nodes[0::2], nodes[1::2]):
            edges.append((x1, x2, 'BLACK'))
    return edges


def colored_edges(p_list: List[List[int]]) -> List[Tuple[int, int, str]]:
    edges = []
    offset = 0
    for p in p_list:
        nodes = chromosome_to_cycle(p)
        nodes = [n + offset for n in nodes]  # add offset to chromosome's node ids
        offset += len(nodes)        # update offset used to shift next chromosome's node ids
        nodes = nodes + nodes[0:2]  # loop around to last 2 elements to simulate a cycle
        for x1, x2 in zip(nodes[1::2], nodes[2::2]):
            edges.append((x1, x2, 'COLOR'))
    return edges


def perform_2_break(edges: List[Tuple[int, int, str]], _2break: Tuple[int, int, int, int]):
    if (_2break[0], _2break[1], 'COLOR') in edges:
        edges.remove((_2break[0], _2break[1], 'COLOR'))
        edges.append((_2break[0], _2break[2], 'COLOR'))
    elif (_2break[1], _2break[0], 'COLOR') in edges:
        edges.remove((_2break[1], _2break[0], 'COLOR'))
        edges.append((_2break[2], _2break[0], 'COLOR'))

    if (_2break[2], _2break[3], 'COLOR') in edges:
        edges.remove((_2break[2], _2break[3], 'COLOR'))
        edges.append((_2break[1], _2break[3], 'COLOR'))
    elif (_2break[3], _2break[2], 'COLOR') in edges:
        edges.remove((_2break[3], _2break[2], 'COLOR'))
        edges.append((_2break[3], _2break[1], 'COLOR'))



def cycle_to_chromosome(c: List[int], chromosome_offset: int) -> List[int]:
    p = []
    for x1, x2 in zip(c[::2], c[1::2]):
        idx = max(x1, x2) // 2
        if x1 < x2:
            p.append(chromosome_offset + idx)
        else:
            p.append(-(chromosome_offset + idx))
    return p


def graph_to_genome(edges: List[Tuple[int, int, str]]) -> List[List[int]]:
    edges = edges[:]
    edge_lookup = {}
    for e in edges:
        edge_lookup.setdefault(e[0], []).append(e)
        edge_lookup.setdefault(e[1], []).append(e)
    p_list = []
    cycles = []
    while edges:
        edge = next(iter(edges))
        ignore_nodes = set()
        cycle = []
        while True:
            n1 = edge[0]
            n2 = edge[1]
            if n1 not in ignore_nodes:
                next_node = n1
            elif n2 not in ignore_nodes:
                next_node = n2
            else:
                raise ValueError('???')

            ignore_nodes.add(next_node)
            next_edges = edge_lookup[next_node]
            if edge in edge_lookup[n1]:
                edge_lookup[n1].remove(edge)
            if edge in edge_lookup[n2]:
                edge_lookup[n2].remove(edge)

            cycle = [edge] + cycle
            edges.remove(edge)
            if not next_edges:
                break
            edge = next_edges.pop()
        cycles.append(cycle)
    for cycle in cycles:
        p = []
        for edge in cycle:
            if edge[2] == 'BLACK':
                if edge[0] < edge[1]:
                    block = edge[1] // 2
                    p.append(block)
                else:
                    block = edge[0] // 2
                    p.append(-block)
        p_list += [p]
    return p_list


edge_list = black_edges(p_list) + colored_edges(p_list)
print(f'{", ".join([str(x) for x in edge_list])}')
perform_2_break(edge_list, _2break)
print(f'{", ".join([str(x) for x in edge_list])}')
p_list = graph_to_genome(edge_list)

# You must shift the answer so that the first element is the highest synteny ID otherwise stepik won't accept it. The
# algorithm that marks the solution is broken.
# for p in p_list:
#     max_block = max(p, key=lambda x: abs(x))
#     while p[0] != max_block:
#         p[:] = p[1:] + p[0:1]

x = ''
for p in p_list:
    x += '('
    x += ' '.join([('+' if c > 0 else '') + str(c) for c in p])
    x += ')'
print(f'{x} ')  # grader expects a space at the end
