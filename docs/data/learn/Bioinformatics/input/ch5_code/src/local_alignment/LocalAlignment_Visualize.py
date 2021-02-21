from local_alignment.LocalAlignment_Graph import create_local_alignment_graph, graph_to_tikz
from WeightLookup import Table2DWeightLookup


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        edge_highlight_str = input()
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
        graph = create_local_alignment_graph(s1, s2, weight_lookup)
        edge_highlights = set()
        if edge_highlight_str != '':  # 0,0->E->1,1|0,0->E->0,1
            for s in edge_highlight_str.split('|'):
                for t1, prefix, t2 in s.split('->'):
                    row1, col1 = t1.split(',')
                    row2, col2 = t2.split(',')
                    found = [e for e in graph.get_edges() if e.startswith(prefix) and graph.get_edge_from(e) == (row1, col1) and graph.get_edge_to(e) == (row2, col2)]
                    if found:
                        edge_highlights.add(found[0])
        output = graph_to_tikz(
            graph,
            edge_highlights
        )
        print(f'````{{latex}}\n{output}\n````', end='\n\n')
        print(f'NOTE: Orange edges are "free rides" from source / Purple edges are "free rides" to sink.', end='\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
