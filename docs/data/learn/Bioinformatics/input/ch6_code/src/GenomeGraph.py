from typing import List, Tuple

from helpers.Utils import slide_window


class GenomeGraph:
    def __init__(self):
        self._node_to_edges = {}
        self._edges = {}
        self._next_edge_id = 0

    def add_permutation(self, permutation: List[int]):
        for (block1, block2), _ in slide_window(permutation, 2, cyclic=True):
            if block1 < 0 and block2 < 0:
                colored_edge1 = (-block1, 'h')
                colored_edge2 = (-block2, 't')
            elif block1 < 0 and block2 > 0:
                colored_edge1 = (-block1, 'h')
                colored_edge2 = (block2, 'h')
            elif block1 > 0 and block2 < 0:
                colored_edge1 = (block1, 't')
                colored_edge2 = (-block2, 't')
            elif block1 > 0 and block2 > 0:
                colored_edge1 = (block1, 't')
                colored_edge2 = (block2, 'h')
            else:
                raise ValueError('ID of 0 not allowed')
            eid = f'E{self._next_edge_id}'
            self._node_to_edges.setdefault(colored_edge1, []).append(eid)
            self._node_to_edges.setdefault(colored_edge2, []).append(eid)
            self._edges[eid] = (colored_edge1, colored_edge2)
            self._next_edge_id += 1

    def all_nodes(self):
        return iter(self._node_to_edges.keys())

    def get_edges(self, nid: Tuple[int, str]):
        return iter(self._node_to_edges[nid])

    def get_edge_endpoints(self, eid: str):
        return self._edges[eid]


if __name__ == '__main__':
    gg = GenomeGraph()
    gg.add_permutation([+1, +2, +3, +4, +5, +6])
    gg.add_permutation([+1, -3, -6, -5])
    gg.add_permutation([+2, -4])

    for nid in gg.get_nodes():
        print(f'{nid}: {[x for x in gg.get_edges(nid)]}')
