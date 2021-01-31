from GlobalAlignment_Graph import create_global_alignment_graph, graph_to_graphviz
from WeightLookup import Constant2DWeightLookup


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        try:
            edge_highlights = {tuple((int(t.split(',')[1]), int(t.split(',')[0])) for t in s.split('->')) for s in input().split('|')}  # 0,0->1,1|0,0->0,1
        except EOFError:
            edge_highlights = set()

        weight_lookup = Constant2DWeightLookup(1.0, 0.0, -1.0)
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
