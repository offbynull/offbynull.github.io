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
# for aa1, aa2 in mismatch_penalties:
#     if aa1 == aa2:
#         mismatch_penalties[(aa1, aa2)] = 1  # 1st negated
#     else:
#         mismatch_penalties[(aa1, aa2)] = -5  # 2nd
# indel_penalty = -1  # 3rd


#
# Load sequences
#
with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')


create_edge_id = unique_id_generator('E')


def populate_up_to_2_columns_of_graph(g, s1, s2):
    grid = []
    s1_list = [None] + s1
    s2_list = ([None] + s2)
    for i, s1_ch in enumerate(s1_list):  # create nodes
        row = []
        for j, s2_ch in enumerate(s2_list[:2]):
            node_id = f'{i}x{j}'
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

def move_subgraph_over_by_1_column(g, s1, s2, next_col: int):
    grid = []
    s1_list = [None] + s1
    s2_list = ([None] + s2)
    for i, _ in enumerate(s1_list):  # delete prev nodes
        g.delete_node(f'{i}x{next_col - 2}')
    for i, s1_ch in enumerate(s1_list):  # create next nodes
        node1_id = f'{i}x{next_col - 1}'
        node2_id = f'{i}x{next_col}'
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


def step(g, s1, s2, col1: int, col2: int, start_row: int):
    grid_rows = len(s1) + 1
    grid_cols = len(s2) + 1

    from_node = f'{start_row}x{col1}'
    assert all([g.get_node_data(g.get_edge_from(e))[0] is not None for e in g.get_inputs(from_node)])  # all predecessor nodes have weights
    to_node = f'{grid_rows-1}x{col2}'
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


def sweep_till_last_col(s1, s2):
    grid_rows = len(s1) + 1
    grid_cols = len(s2) + 1
    g = Graph()

    populate_up_to_2_columns_of_graph(g, s1, s2)
    root_node_data = g.get_node_data(f'{0}x{0}')
    root_node_data[0] = 0
    if grid_cols == 1:
        step(g, s1, s2, col1=0, col2=0, start_row=0)
        found_row, _ = max([(r, g.get_node_data(f'{r}x0')[0]) for r in range(grid_rows)], key=lambda e: e[1])
    else:
        step(g, s1, s2, col1=0, col2=1, start_row=0)
        found_row, _ = max([(r, g.get_node_data(f'{r}x1')[0]) for r in range(grid_rows)], key=lambda e: e[1])
        for c in range(2, grid_cols):
            move_subgraph_over_by_1_column(g, s1, s2, next_col=c)
            step(g, s1, s2, col1=c - 1, col2=c, start_row=found_row)
            found_row, _ = max([(r, g.get_node_data(f'{r}x{c}')[0]) for r in range(grid_rows)], key=lambda e: e[1])
    last_col_vals = [g.get_node_data(f'{r}x{grid_cols - 1}')[0] for r in range(grid_rows)]

    return last_col_vals


def find_middle_nodes(s1, s2, col_idx = None):
    if col_idx is None:
        col_idx = len(s2) // 2
    left_sweep_final_col_weights = sweep_till_last_col(s1, s2[:col_idx])
    right_sweep_final_col_weights = sweep_till_last_col(s1[::-1], s2[col_idx - 1:][::-1])[::-1]
    # print(f'{left_sweep_final_col_weights}')
    # print(f'{right_sweep_final_col_weights}')
    combined_sweep_final_col_weights = [v1 + v2 for v1, v2 in zip(left_sweep_final_col_weights, right_sweep_final_col_weights)]
    # print(f'{combined_sweep_final_col_weights}')
    max_combined_weight = max(combined_sweep_final_col_weights)
    max_combined_weight_idxes = [i for i, v in enumerate(combined_sweep_final_col_weights) if v == max_combined_weight]
    return (max_combined_weight_idxes[0], col_idx, max_combined_weight_idxes[0])


def find_middle_edge(s1, s2, node):
    s1_idx = node[0] - 1
    s2_idx = node[1] - 1
    weight = node[2]
    right = (weight + indel_penalty, '→')
    down = (weight + indel_penalty, '↓')
    diag = (weight + mismatch_penalties[(s1[s1_idx + 1], s2[s2_idx + 1])], '↘')
    return max([right, down, diag])


def linear_space_alignment(v, w, top, bottom, left, right, output):
    if left == right:
        for i in range(top, bottom):
            output += ['↓']
        return
    if top == bottom:
        for i in range(left, right):
            output += ['→']
        return

    s1_target = s1[top:bottom]
    s2_target = s2[left:right]
    middle_node = find_middle_nodes(s1_target, s2_target)
    _, edge_dir = find_middle_edge(s1_target, s2_target, middle_node)
    upper_region_end_row = top + middle_node[0]
    upper_region_end_col = left + middle_node[1]
    linear_space_alignment(v, w, top, upper_region_end_row, left, upper_region_end_col, output)
    output += [edge_dir]
    if edge_dir == '→':
        lower_region_end_row, lower_region_end_col = upper_region_end_row, upper_region_end_col + 1
    elif edge_dir == '↓':
        lower_region_end_row, lower_region_end_col = upper_region_end_row + 1, upper_region_end_col
    elif edge_dir == '↘':
        lower_region_end_row, lower_region_end_col = upper_region_end_row + 1, upper_region_end_col + 1
    else:
        raise ValueError()
    linear_space_alignment(v, w, lower_region_end_row, bottom, lower_region_end_col, right, output)


I THINK FIND_MIDDLE_NODES IS CORRECT BUT FIND_MIDDLE_EDGES IS STILL WRONG -- TO FIND THE CORRECT MIDDLE EDGE, YOU NEED
TO PROCESS 1 COLUMN PAST THE MIDDLE COLUMN. IF THE NODES THAT THE MIDDLE NODE POINTS TO IN THAT NEXT COLUMN, THE NODE
WITH THE LARGEST WEIGHT IS THE WHERE THE EDGE IS BETWEEN. RIGHT NOW YOU'RE USING THE EDGE WEIGHTS, WHICH IS INCORRECT
-- THE OUTGOING EDGE WITH MAX WEIGHT DOESN'T MEAN THAT THE NODE ITS POINTING TO WILL HAVE THE MAX WEIGHT AS WELL (IT
HAS OTHER EDGES POINTING TO IT)

FIX MIDDLEEDGEINLIENEARSPACE CODECHALLENGE FIRST

s1 = list(lines[0].strip())
s2 = list(lines[1].strip())
print(f'{find_middle_nodes(s1, s2, 1)}')
print(f'{find_middle_edge(s1, s2, find_middle_nodes(s1, s2, 0))}')
# output = []
# linear_space_alignment(s1, s2, 0, len(s1), 0, len(s2), output)
# print(f'{output}')
#
# s1.pop(0)
# s2.pop(0)
# s1_align = ''
# s2_align = ''
# weight = 0
# for edge_dir, edge_weight in output:
#     weight += edge_weight
#     if edge_dir == '↓':
#         s1_align += s1.pop(0)
#         s2_align += '-'
#     elif edge_dir == '↘':
#         s1_align += s1.pop(0)
#         s2_align += s2.pop(0)
#     elif edge_dir == '→':
#         s1_align += '-'
#         s2_align += s2.pop(0)
#     else:
#         raise ValueError()
#
# print(weight)
# print(s1_align)
# print(s2_align)