from collections import Counter
from typing import List, TypeVar

from Graph import Graph
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair
from Utils import slide_window

T = TypeVar('T')


# MARKDOWN
def to_debruijn_graph(reads: List[T], skip: int = 1) -> Graph[T]:
    graph = Graph()
    for read in reads:
        from_node = read.prefix(skip)
        to_node = read.suffix(skip)
        graph.insert_edge(from_node, to_node)
    return graph
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
                   + ' [label="' + str(node.append_overlap(to_node)) + '"];\n'
    return 'digraph {\n'\
           + 'graph[rankdir=LR, center=true, margin=0.2, nodesep=0.15, ranksep=0.1]\n'\
           + 'node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]\n'\
           + 'edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, fixedsize=true, arrowhead=vee]\n'\
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
        graph = to_debruijn_graph(frags)
        print(f'Given the fragments {lines}, the de Bruijn graph is...', end="\n\n")
        print(f'```{{dot}}\n{to_graphviz(graph)}\n```\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()


# If we gave you the de Bruijn graph DeBruijn_k(Text) without giving you Text, could you reconstruct Text?
#   YES. don't walk over same edge more than once

# Construct the de Bruijn graphs DeBruijn_2(TAATGCCATGGGATGTT), DeBruijn_3(TAATGCCATGGGATGTT), and DeBruijn_4(TAATGCCATGGGATGTT). What do you notice?
#   LOWER K: more connections per node, more cycles, less nodes
#   HIGHER K: less connections per node, less cycles, more nodes
# nodes = to_debruijn_graph_from_genome_path(2, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
# print('---')
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
# print('---')
# nodes = to_debruijn_graph_from_genome_path(4, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')

# How does the graph DeBruijn_3(TAATGCCATGGGATGTT) compare to DeBruijn_3(TAATGGGATGCCATGTT)?
#    SAME GRAPH.
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGCCATGGGATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
# print('---')
# nodes = to_debruijn_graph_from_genome_path(3, 'TAATGGGATGCCATGTT')
# for kmer, other_kmers in nodes.items():
#     print(f'{kmer} -> {",".join(other_kmers)}')
