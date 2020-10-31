from collections import Counter
from typing import List, TypeVar

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair

T = TypeVar('T', Read, ReadPair)


# MARKDOWN
def to_overlap_graph(items: List[T], skip: int = 1) -> Graph[T]:
    ret = Graph()

    prefixes = dict()
    suffixes = dict()
    for i, item in enumerate(items):
        prefix = item.prefix(skip)
        prefixes.setdefault(prefix, set()).add(i)
        suffix = item.suffix(skip)
        suffixes.setdefault(suffix, set()).add(i)

    for key, indexes in suffixes.items():
        other_indexes = prefixes.get(key)
        if other_indexes is None:
            continue
        for i in indexes:
            item = items[i]
            for j in other_indexes:
                if i == j:
                    continue
                other_item = items[j]
                ret.insert_edge(item, other_item)
    return ret
# MARKDOWN


def to_graphviz(g: Graph) -> str:
    out = ''
    for node, to_nodes in g._outbound.items():
        for to_node in to_nodes.elements():
            from_node_str = str(node) + ' [' + str(node.instance) + ']'
            to_node_str = str(to_node) + ' [' + str(to_node.instance) + ']'
            out += '"' + from_node_str.replace("\"", "\\\"") + '\"'\
                   + ' -> '\
                   + '"' + to_node_str.replace("\"", "\\\"") + '"'\
                   + ' [shape=plain];\n'
    return 'digraph {\n'\
           + 'graph[rankdir=LR, center=true, margin=0.2, nodesep=0.15, ranksep=0.1]\n'\
           + 'node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]\n'\
           + 'edge[arrowsize=0.6, arrowhead=vee]\n'\
           + out\
           + '}\n'


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
        print(f'```{{dot}}\n{to_graphviz(graph)}\n```\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
