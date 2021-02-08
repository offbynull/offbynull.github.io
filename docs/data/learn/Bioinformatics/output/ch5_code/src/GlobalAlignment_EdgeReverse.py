from itertools import product
from textwrap import dedent
from typing import Tuple, Set

from FindMaxPath_DPBacktrack import populate_weights_and_backtrack_pointers, backtrack
from GlobalAlignment_Graph import create_global_alignment_graph, NodeData, EdgeData
from Graph import Graph
from WeightLookup import Table2DWeightLookup
from helpers.Utils import latex_escape


def flip_graph(graph: Graph):
    flipped_graph = Graph()
    for n_id in graph.get_nodes():
        n_data = graph.get_node_data(n_id)
        flipped_graph.insert_node(n_id, n_data)
    for e_id in graph.get_edges():
        from_n_id, to_n_id, e_data = graph.get_edge(e_id)
        flipped_graph.insert_edge(e_id, to_n_id, from_n_id, e_data)
    return flipped_graph


def graph_to_tikz(
        graph: Graph[Tuple[int, ...], NodeData, str, EdgeData],
        highlight_edges: Set[str],
        scale_x: float = 3.75,
        scale_y: float = 3.75,
        caption: str = ''
) -> str:
    layers = set(n[:-2] for n in graph.get_nodes())
    row_len = max(n[-2] for n in graph.get_nodes()) + 1
    col_len = max(n[-1] for n in graph.get_nodes()) + 1
    ret = dedent(f'''
        \\begin{{tikzpicture}}
        \\node[anchor=west] at (0, 1.5) (header) {{{latex_escape(caption)}}};
    ''')
    node_id_to_latex_id = {}
    for node_id_prefix in layers:
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            node_id_to_latex_id[node_id] = 'N' + '_'.join(str(c) for c in node_id)
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            node_data = graph.get_node_data(node_id)
            node_label = f'{node_data.weight}'
            row_pos = node_id_suffix[0] * scale_x
            col_pos = -node_id_suffix[1] * scale_y
            ret += f'        \\node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at ({row_pos}, {col_pos}) ({node_id_to_latex_id[node_id]}) {{{latex_escape(node_label)}}};\n'
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            if not graph.has_node(node_id):
                continue
            for edge_id in graph.get_outputs(node_id):
                child_node_id = graph.get_edge_to(edge_id)
                child_node_id_prefix = child_node_id[:-2]
                if child_node_id_prefix != node_id_prefix:
                    continue
                edge_data = graph.get_edge_data(edge_id)
                edge_color = 'gray!40'
                if edge_id in highlight_edges:
                    edge_color = 'green'
                edge_label = f'{"—" if edge_data.v_elem is None else edge_data.v_elem}\\\\ {"—" if edge_data.w_elem is None else edge_data.w_elem}\\\\ {edge_data.weight}'
                ret += f'        \\draw[->, >=stealth, line width = 2px, {edge_color}]' \
                       f' ({node_id_to_latex_id[node_id]})' \
                       f' to' \
                       f' []' \
                       f' node [align=center, midway, color=black] {{{edge_label}}}' \
                       f' ({node_id_to_latex_id[child_node_id]});\n'
    ret += dedent('''
        \\end{tikzpicture}
    ''')
    return ret


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        matrix_type = input()
        if matrix_type == 'embedded_score_matrix':
            indel_weight = float(input())
            weights_data = ''
            try:
                while True:
                    weights_data += input() + '\n'
            except EOFError:
                ...
        elif matrix_type == 'file_score_matrix':
            indel_weight = float(input())
            path = input()
            with open(path, mode='r', encoding='utf-8') as f:
                weights_data = f.read()
        else:
            raise ValueError('Bad score matrix type')
        weight_lookup = Table2DWeightLookup.create_from_str(weights_data, indel_weight)
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        graph = create_global_alignment_graph(s1, s2, weight_lookup)
        populate_weights_and_backtrack_pointers(
            graph,
            (0, 0),
            lambda n_id, weight, e_id: graph.get_node_data(n_id).set_weight_and_backtracking_edge(weight, e_id),
            lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
            lambda e_id: graph.get_edge_data(e_id).weight
        )
        graph_edges = backtrack(
            graph,
            (len(s1), len(s2)),
            lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge()
        )
        graph_output = graph_to_tikz(graph, set(graph_edges), caption='Original')
        flipped_graph = flip_graph(graph)
        populate_weights_and_backtrack_pointers(
            flipped_graph,
            (len(s1), len(s2)),
            lambda n_id, weight, e_id: graph.get_node_data(n_id).set_weight_and_backtracking_edge(weight, e_id),
            lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
            lambda e_id: graph.get_edge_data(e_id).weight
        )
        # flipped_graph_edges = backtrack(
        #     flipped_graph,
        #     (0, 0),
        #     lambda n_id: flipped_graph.get_node_data(n_id).get_weight_and_backtracking_edge()
        # )
        flipped_graph_edges = graph_edges  # if you backtracked flipped_graph, the edges would be exactly the same (verified below)
        assert flipped_graph.get_node_data((0, 0)).weight == sum(flipped_graph.get_edge_data(e_id).weight for e_id in flipped_graph_edges)  # flipped_graph's (0, 0) node is the sink node
        flipped_graph_output = graph_to_tikz(flipped_graph, set(flipped_graph_edges), caption='Reversed Edge')
        combined_output = dedent(f'''
        \\documentclass{{standalone}}
        \\usepackage{{tikz, pagecolor}}
        \\begin{{document}}
            \\pagecolor{{white}}
            {graph_output}
            \\hspace{{3cm}}
            {flipped_graph_output}
        \\end{{document}}
        ''')
        print(f'Left is original, right is reversed edges: \n\n````{{latex}}\n{combined_output}\n````', end='\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
