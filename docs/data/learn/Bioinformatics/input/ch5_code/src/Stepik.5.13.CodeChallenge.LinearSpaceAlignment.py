from collections import Counter
from typing import Dict, Tuple

from Graph import Graph
from helpers.Utils import slide_window, unique_id_generator

#
# Load scoring matrix
#
indel_penalty = -5  # specified in problem statement
mismatch_penalties: Dict[Tuple[str, str], int] = {}
with open('BLOSUM62.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = data.strip().split('\n')
aa_row = lines[0].strip().split()
for line in lines[1:]:
    vals = line.strip().split()
    aa2 = vals[0]
    weight = vals[1:]
    for aa1, weight in zip(aa_row, weight):
        mismatch_penalties[(aa1, aa2)] = int(weight)


#
# Load sequences
#
with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')


STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN
STILL BROKEN


def get_middle_edge(s1, s2, top, bottom, left, right):
    # THIS ONLY CALCULATES THE MAX WEIGHT OF THE PATH IN A LARGE SEQUENCE ALIGNMENT GRAPH (not the path itself, just the
    # weight of the path) -- IT DOES SO BY ONLY LOADING ENOUGH OF THE GRAPH TO PROCESS THE NEXT STEP. Also, this calculates
    # the path up until the middle column + 1, not until the end of the graph.

    create_edge_id = unique_id_generator('E')
    g = Graph()

    print(f' {s2[left:right+1]}')
    [print(ch) for ch in s1[top:bottom+1]]
    print('')

    def populate_initial_2_columns_of_graph():
        grid = []
        s1_list = s1
        s2_list = s2
        for i, s1_ch in enumerate(s1_list[top:bottom+1]):  # create nodes
            row = []
            for j, s2_ch in enumerate(s2_list[left:left+2]):
                node_id = f'{top+i}x{left+j}'
                row.append(node_id)
                g.insert_node(node_id, [None, s1_ch, s2_ch])
            grid.append(row)
        for row in grid:  # create horizontal edges
            for node_pair, _ in slide_window(row, 2):
                src_n, dst_n = node_pair
                g.insert_edge(create_edge_id(), src_n, dst_n, indel_penalty)
        for row_pair, _ in slide_window(grid, 2):  # create vertical edges
            row1, row2 = row_pair
            for src_n, dst_n in zip(row1, row2):
                g.insert_edge(create_edge_id(), src_n, dst_n, indel_penalty)
        for row_pair, _ in slide_window(grid, 2):  # create diagonal edges
            row1, row2 = row_pair
            for src_n, dst_n in zip(row1[:-1], row2[1:]):
                _, dst_n_s1_ch, dst_n_s2_ch = g.get_node_data(dst_n)
                penalty = mismatch_penalties[(dst_n_s1_ch, dst_n_s2_ch)]
                g.insert_edge(create_edge_id(), src_n, dst_n, penalty)

    def move_subgraph_over_by_1_column(next_col: int):
        grid = []
        s1_list = s1
        s2_list = s2
        for r in range(top, bottom + 1):  # delete prev nodes
            g.delete_node(f'{r}x{next_col - 2}')
        for r, s1_ch in zip(range(top, bottom + 1), s1_list[top:bottom + 1]):  # create next nodes
            node1_id = f'{r}x{next_col - 1}'
            node2_id = f'{r}x{next_col}'
            row = [node1_id, node2_id]
            grid.append(row)
            g.insert_node(node2_id, [None, s1_ch, s2_list[next_col]])
        for row in grid:  # create horizontal edges
            for node_pair, _ in slide_window(row, 2):
                src_n, dst_n = node_pair
                g.insert_edge(create_edge_id(), src_n, dst_n, indel_penalty)
        for row_pair, _ in slide_window(grid, 2):  # create vertical edges for NEWLY created nodes (prev has them already)
            row1, row2 = row_pair
            src_n, dst_n = row1[1], row2[1]
            g.insert_edge(create_edge_id(), src_n, dst_n, indel_penalty)
        for row_pair, _ in slide_window(grid, 2):  # create diagonal edges
            row1, row2 = row_pair
            for src_n, dst_n in zip(row1[:-1], row2[1:]):
                _, dst_n_s1_ch, dst_n_s2_ch = g.get_node_data(dst_n)
                penalty = mismatch_penalties[(dst_n_s1_ch, dst_n_s2_ch)]
                g.insert_edge(create_edge_id(), src_n, dst_n, penalty)

    def step(col1: int, col2: int, start_row: int):
        from_node = f'{start_row}x{col1}'
        assert all([g.get_node_data(g.get_edge_from(e))[0] is not None for e in
                    g.get_inputs(from_node)])  # all predecessor nodes have weights
        to_node = f'{bottom}x{col2}'
        assert g.get_out_degree(to_node) == 0

        complete_nodes = {n for n in g.get_nodes() if g.get_node_data(n)[0] is not None}
        waiting_nodes = set()
        for node in complete_nodes:
            for e in g.get_outputs(node):
                dst_node = g.get_edge_to(e)
                if dst_node in complete_nodes:
                    continue
                if {g.get_edge_from(e) for e in g.get_inputs(dst_node)}.issubset(complete_nodes):
                    waiting_nodes |= {dst_node}

        from_node_data = g.get_node_data(from_node)
        from_node_data[0] = 0

        remaining_unprocessed_inputs_for_each_node = Counter()
        for node in g.get_nodes():
            incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
            incoming_nodes -= complete_nodes
            remaining_unprocessed_inputs_for_each_node[node] = len(incoming_nodes)

        while len(waiting_nodes) > 0:
            node = next(iter(waiting_nodes))
            incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(node)}
            if not incoming_nodes.issubset(complete_nodes):
                continue
            incoming_accum_weights = []
            for edge in g.get_inputs(node):
                src_node = g.get_edge_from(edge)
                src_node_weight, _, _ = g.get_node_data(src_node)
                edge_weight = g.get_edge_data(edge)
                # Roots that aren't from_node were initialized to a weight of None -- if you see them, skip them.
                if src_node_weight is not None:
                    incoming_accum_weights += [src_node_weight + edge_weight]
            if len(incoming_accum_weights) == 0:
                max_weight = None
            else:
                max_weight = max(incoming_accum_weights)
            node_data = g.get_node_data(node)
            node_data[0] = max_weight
            # This node has been processed, move it over to complete_nodes.
            waiting_nodes.remove(node)
            complete_nodes.add(node)
            # For outgoing nodes this node points to, if that outgoing node has all of its dependencies in complete_nodes,
            # then add it to waiting_nodes (so it can be processed).
            outgoing_nodes = {g.get_edge_to(e) for e in g.get_outputs(node)}
            for output_node in outgoing_nodes:
                remaining_unprocessed_inputs_for_each_node[output_node] -= 1
                if remaining_unprocessed_inputs_for_each_node[output_node] == 0:
                    waiting_nodes.add(output_node)

    populate_initial_2_columns_of_graph()
    root_node_data = g.get_node_data(f'{top}x{left}')
    root_node_data[0] = 0
    step(col1=left, col2=left+1, start_row=top)
    found_row, _ = max([(r, g.get_node_data(f'{r}x{left + 1}')[0]) for r in range(top, bottom+1)], key=lambda e: e[1])

    # Calculate up until middle column PLUS one
    middle_col_idx = left + ((right - left) // 2)
    for c in range(left + 1, middle_col_idx):
        move_subgraph_over_by_1_column(next_col=c+1)
        step(col1=c, col2=c+1, start_row=found_row)
        found_row, _ = max([(r, g.get_node_data(f'{r}x{c}')[0]) for r in range(top, bottom+1)], key=lambda e: e[1])
    row_in_middle_col = found_row

    if right >= left + 2:
        move_subgraph_over_by_1_column(next_col=middle_col_idx+1)
        step(col1=middle_col_idx, col2=middle_col_idx+1, start_row=row_in_middle_col)
        row_in_next_col, _ = max([(r, g.get_node_data(f'{r}x{middle_col_idx+1}')[0]) for r in range(top, bottom+1)], key=lambda e: e[1])

    # Calculate the node in the next column that the middle node points to
    middle_node_id = f'{row_in_middle_col}x{middle_col_idx}'
    max_edge_weight = None
    max_edge_src_node_id = None
    max_edge_dst_node_id = None
    for edge in g.get_outputs(f'{middle_node_id}'):
        from_node_id, to_node_id, weight = g.get_edge(edge)
        if max_edge_weight is None or weight > max_edge_weight:
            max_edge_src_node_id = from_node_id
            max_edge_dst_node_id = to_node_id
            max_edge_weight = weight
    max_neighbour_row, max_neighbour_col = [int(x) for x in max_edge_dst_node_id.split('x')]

    if row_in_middle_col == max_neighbour_row:
        next_dir = '→'
    elif row_in_middle_col + 1 == max_neighbour_row:
        next_dir = '↘'
    else:
        raise ValueError('This should never happen')

    return max_edge_src_node_id, max_edge_dst_node_id, next_dir, max_edge_weight


def linear_space_alignment(v, w, top, bottom, left, right, output):
    if left == right:
        for i in range(top, bottom):
            output += [('↓', indel_penalty)]
        return
    if top == bottom:
        for i in range(left, right):
            output += [('→', indel_penalty)]
        return
    mid_edge_src, mid_edge_dst, mid_edge_dir, mid_edge_weight = get_middle_edge(v, w, top, bottom, left, right)
    print(f'{mid_edge_src} to {mid_edge_dst}, edge: {mid_edge_dir}')
    upper_region_end_row = int(mid_edge_src.split('x')[0])
    upper_region_end_col = int(mid_edge_src.split('x')[1])
    linear_space_alignment(v, w, top, upper_region_end_row, left, upper_region_end_col, output)
    output += [(mid_edge_dir, mid_edge_weight)]
    lower_region_end_row = int(mid_edge_dst.split('x')[0])
    lower_region_end_col = int(mid_edge_dst.split('x')[1])
    linear_space_alignment(v, w, lower_region_end_row, bottom, lower_region_end_col, right, output)



s1 = [None] + list(lines[0].strip())
s2 = [None] + list(lines[1].strip())
output = []
linear_space_alignment(s1, s2, 0, len(s1) - 1, 0, len(s2) - 1, output)

print(f'{output}')

s1.pop(0)
s2.pop(0)
s1_align = ''
s2_align = ''
weight = 0
for edge_dir, edge_weight in output:
    weight += edge_weight
    if edge_dir == '↓':
        s1_align += s1.pop(0)
        s2_align += '-'
    elif edge_dir == '↘':
        s1_align += s1.pop(0)
        s2_align += s2.pop(0)
    elif edge_dir == '→':
        s1_align += '-'
        s2_align += s2.pop(0)
    else:
        raise ValueError()

print(weight)
print(s1_align)
print(s2_align)