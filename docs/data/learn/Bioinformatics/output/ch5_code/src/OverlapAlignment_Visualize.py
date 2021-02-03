from LocalAlignment_Graph import graph_to_graphviz
from OverlapAlignment_Graph import create_overlap_alignment_graph
from WeightLookup import Table2DWeightLookup


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
        graph = create_overlap_alignment_graph(s1, s2, weight_lookup)
        output = graph_to_graphviz(
            graph,
            edge_highlights,
            scale_x=1.75,
            scale_y=1.75
        )
        print(f'````{{graphvizFdp}}\n{output}\n````', end='\n\n')
        print(f'NOTE: Orange edges are free rides from source / Purple edges are free rides to sink. No text associated with free rides.', end='\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
