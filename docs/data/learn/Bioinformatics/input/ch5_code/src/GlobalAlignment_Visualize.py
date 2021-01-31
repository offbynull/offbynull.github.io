from GlobalAlignment_Graph import create_global_alignment_graph, graph_to_graphviz
from WeightLookup import Constant2DWeightLookup, Table2DWeightLookup


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        edge_highlight_str = input()
        if edge_highlight_str != '':
            edge_highlights = {tuple((int(t.split(',')[1]), int(t.split(',')[0])) for t in s.split('->')) for s in edge_highlight_str.split('|')}  # 0,0->1,1|0,0->0,1
        else:
            edge_highlights = set()
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
        graph = create_global_alignment_graph(s1, s2, weight_lookup)
        output = graph_to_graphviz(
            graph,
            get_edge_label_func=lambda ed: f'{"-" if ed.v_elem is None else ed.v_elem}\n{"-" if ed.w_elem is None else ed.w_elem}\n{ed.weight}',
            is_edge_highlight_func=lambda e: e.startswith('E') and (graph.get_edge_from(e), graph.get_edge_to(e)) in edge_highlights,
            get_node_label_func=lambda nd: "",
            scale_x=1.75,
            scale_y=1.75
        )
        print(f'````{{graphvizFdp}}\n{output}\n````', end='\n\n')
        print(f'NOTE: Each edge is labeled with the elements selected from the 1st sequence, 2nd sequence, and edge weight.', end='\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
