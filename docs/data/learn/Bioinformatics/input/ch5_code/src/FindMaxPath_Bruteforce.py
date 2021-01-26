from typing import TypeVar, Callable, Tuple, List, Optional

from Graph import Graph
from GraphvizRender import graph_to_graphviz
from helpers.Utils import unique_id_generator

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')

ELEM = TypeVar('ELEM')

GET_EDGE_WEIGHT_FUNC_TYPE =\
    Callable[
        [
            E                  # edge ID
        ],
        float                  # edge weight
    ]


# MARKDOWN
def find_max_path(
        graph: Graph[N, ND, E, ED],
        current_node: N,
        end_node: N,
        get_edge_weight_func: GET_EDGE_WEIGHT_FUNC_TYPE
) -> Optional[Tuple[List[N], float]]:
    if current_node == end_node:
        return [end_node], 0.0
    alternatives = []
    for edge_id in graph.get_outputs(current_node):
        edge_weight = get_edge_weight_func(edge_id)
        child_n = graph.get_edge_to(edge_id)
        res = find_max_path(
            graph,
            child_n,
            end_node,
            get_edge_weight_func
        )
        if res is None:
            continue
        path, weight = res
        path = [current_node] + path
        weight = edge_weight + weight
        res = path, weight
        alternatives.append(res)
    if len(alternatives) == 0:
        return None  # no path to end, so return None
    else:
        return max(alternatives, key=lambda x: x[1])  # choose path to end with max weight
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        edges = [tuple(v for v in s.split()) for s in input().split(",")]
        nodes = {n1 for n1, _, _ in edges} | {n2 for _, n2, _ in edges}
        graph = Graph()
        for n in nodes:
            graph.insert_node(n)
        edge_id_gen_func = unique_id_generator('E')
        for n1, n2, weight in edges:
            graph.insert_edge(edge_id_gen_func(), n1, n2, float(weight))
        from_node = input()
        to_node = input()
        print(f'Given the following graph...', end="\n\n")
        print(f'````{{dot}}\n{graph_to_graphviz(graph, lambda e: str(e))}\n````', end='\n\n')
        path, weight = find_max_path(
            graph,
            from_node,
            to_node,
            lambda edge_id: graph.get_edge_data(edge_id)
        )
        print(f'... the path with the max weight between {from_node} and {to_node} ...', end='\n')
        print(f' * Maximum path = {" -> ".join(path)}', end='\n')
        print(f' * Maximum weight = {weight}', end='\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
