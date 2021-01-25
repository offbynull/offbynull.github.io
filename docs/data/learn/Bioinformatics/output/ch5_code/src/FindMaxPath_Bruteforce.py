import math
from typing import TypeVar, Callable, Tuple, List

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
FOUND_PATH_FUNC_TYPE =\
    Callable[
        [
            List[N],
            float
        ],
        None
    ]


# MARKDOWN
def walk(
        g: Graph[N, ND, E, ED],
        end_node: N,
        current_node: N,
        current_path: List[N],
        current_weight: float,
        get_edge_weight_func: GET_EDGE_WEIGHT_FUNC_TYPE,
        found_path_func: FOUND_PATH_FUNC_TYPE
):
    if current_node == end_node:
        found_path_func(current_path, current_weight)
        return
    for edge_id in g.get_outputs(current_node):
        edge_weight = get_edge_weight_func(edge_id)
        child_n = g.get_edge_to(edge_id)
        walk(
            g,
            end_node,
            child_n,
            current_path + [child_n],
            current_weight + edge_weight,
            get_edge_weight_func,
            found_path_func
        )


def find_max_path(
        g: Graph[N, ND, E, ED],
        from_node: N,
        to_node: N,
        get_edge_data_func: GET_EDGE_WEIGHT_FUNC_TYPE
) -> Tuple[List[N], float]:
    last_path = []
    last_weight = -math.inf

    def overwrite_max_func(path: List[N], weight: float):
        nonlocal  last_path, last_weight
        if weight > last_weight:
            last_weight = weight
            last_path = path

    walk(g, to_node, from_node, [from_node], 0.0, get_edge_data_func, overwrite_max_func)
    return last_path, last_weight
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
