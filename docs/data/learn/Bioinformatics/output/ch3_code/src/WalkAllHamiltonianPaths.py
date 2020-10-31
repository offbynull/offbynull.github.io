from collections import Counter
from typing import List, TypeVar

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair
from ToOverlapGraphHash import to_overlap_graph, to_graphviz
from Utils import slide_window_kd

T = TypeVar('T')


# MARKDOWN
def exhaustively_walk_until_all_nodes_touched_exactly_one(
        graph: Graph[T],
        from_node: T,
        current_path: List[T]
) -> List[List[T]]:
    current_path.append(from_node)

    if len(current_path) == len(graph):
        found_paths = [current_path.copy()]
    else:
        found_paths = []
        for to_node in graph.get_outputs(from_node):
            if to_node in set(current_path):
                continue
            found_paths += exhaustively_walk_until_all_nodes_touched_exactly_one(graph, to_node, current_path)

    current_path.pop()
    return found_paths


# walk each node exactly once
def walk_hamiltonian_paths(graph: Graph[T], from_node: T) -> List[List[T]]:
    return exhaustively_walk_until_all_nodes_touched_exactly_one(graph, from_node, [])
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input().strip()
                if len(line) > 0:
                    lines.append(line)
            except EOFError:
                break

        command = lines[0]
        lines = lines[1:]
        counter = Counter(lines)
        if command == 'reads':
            frags = [Read(r, i) for r, c in counter.items() for i in range(c)]
        elif command == 'read-pairs':
            frags = [ReadPair(Kdmer(r.split('|')[0], r.split('|')[2], int(r.split('|')[1])), i) for r, c in counter.items() for i in range(c)]
        else:
            raise
        graph = to_overlap_graph(frags)
        print(f'Given the fragments {lines}, the overlap graph is...', end="\n\n")
        print(f'```{{dot}}\n{to_graphviz(graph)}\n```', end="\n\n")
        print(f'... and the Hamiltonian paths are ...', end="\n\n")
        all_paths = set([tuple(path) for node in graph.get_nodes() for path in walk_hamiltonian_paths(graph, node)])
        for path in all_paths:
            print(f' * {" -> ".join([str(p) for p in path])}')

    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()