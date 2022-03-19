from __future__ import annotations

from typing import TypeVar, Generic, Iterator, Optional, Callable

# Adapted from the graph class I built to solve chapter 3 problems (genome assembly)
from graph import DirectedGraph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')


class Graph(Generic[N, ND, E, ED]):
    def __init__(self):
        self._node_outbound: dict[N, set[E]] = {}
        self._node_data: dict[N, ND] = {}
        self._edges: dict[E, (N, N, ED)] = {}

    def insert_node(self: Graph, node: N, data: Optional[ND] = None):
        assert node not in self._node_outbound  # if it's not in outbound, it won't be in inbound as well
        self._node_outbound[node] = set()
        self._node_data[node] = data

    def delete_node(self: Graph, node: N):
        assert node in self._node_outbound
        for edge_id in self._node_outbound[node].copy():
            lt_node, gt_node, _ = self._edges[edge_id]
            self._node_outbound[lt_node].remove(edge_id)
            self._node_outbound[gt_node].remove(edge_id)
            del self._edges[edge_id]
        # _node_inbound mirrors _node_outbound, so you don't have to do the above again for _node_inbound
        del self._node_outbound[node]
        del self._node_data[node]

    def update_node_data(self: Graph, node: N, data: Optional[ND] = None):
        assert node in self._node_outbound  # if it's not in outbound, it won't be in inbound as well
        self._node_data[node] = data

    def get_node_data(self: Graph, node: N) -> Optional[ND]:
        assert node in self._node_outbound
        return self._node_data[node]

    def insert_edge(
            self: Graph,
            edge: E,
            node1: N,
            node2: N,
            data: Optional[ED] = None):
        assert node1 in self._node_outbound
        assert node2 in self._node_outbound
        assert edge not in self._edges
        [lt_node, gt_node] = sorted([node1, node2])
        self._edges[edge] = (node1, node2, data)
        self._node_outbound[lt_node].add(edge)
        self._node_outbound[gt_node].add(edge)

    def delete_edge(
            self: Graph,
            edge: E,
            remove_if_isolated: bool = False):
        assert edge in self._edges
        lt_node, gt_node, _ = self._edges[edge]
        assert lt_node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        assert gt_node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        self._node_outbound[lt_node].remove(edge)
        self._node_outbound[gt_node].remove(edge)
        # from and to may be the same -- if they are, and you've removed the from, make sure you don't try to remove to
        # because form and to are the same... you can't remove the same node twice
        dealing_with_same_node = lt_node == gt_node
        removed_already = False
        if remove_if_isolated\
                and len(self._node_outbound[lt_node]) == 0:
            self.delete_node(lt_node)
            removed_already = True
        if remove_if_isolated\
                and len(self._node_outbound[gt_node]) == 0 \
                and (not dealing_with_same_node or (dealing_with_same_node and not removed_already)):
            self.delete_node(gt_node)
        del self._edges[edge]

    # updates the data for the FIRST edge b
    def update_edge_data(
            self: Graph,
            edge: E,
            data: Optional[ED] = None):
        lt_node, gt_node, _ = self._edges[edge]
        self.delete_edge(edge)
        self.insert_edge(edge, lt_node, gt_node, data)

    def get_edge_data(self: Graph, edge: E) -> Optional[ED]:
        return self._edges[edge][2]

    def get_edge_ends(self: Graph, edge: E) -> tuple[N, N]:
        e = self._edges[edge]
        return e[0], e[1]

    def get_edge_end(self: Graph, edge: E, skip_node: N) -> N:
        e = self._edges[edge]
        if skip_node == e[0]:
            return e[1]
        elif skip_node == e[1]:
            return e[0]
        raise ValueError(f'{skip_node} not at either end of {edge}')

    def get_edge(self: Graph, edge: E) -> tuple[N, N, ED]:
        return self._edges[edge]

    def get_leaf_nodes(self: Graph) -> Iterator[N]:
        return (n for n in self.get_nodes() if self.get_degree(n) == 1)

    def get_nodes(self: Graph) -> Iterator[N]:
        return iter(self._node_outbound)

    def get_edges(self: Graph) -> Iterator[E]:
        return iter(self._edges)

    def has_node(self: Graph, node: N) -> bool:
        return node in self._node_outbound  # inbound and outbound are reflections of each other, so only check one

    def has_edge(self: Graph, edge: E) -> bool:
        return edge in self._edges  # inbound and outbound are reflections of each other, so only check one

    def get_outputs_full(
            self: Graph,
            node: N,
            predicate: Callable[[E, ED | None], bool] | None = None
    ) -> Iterator[tuple[E, N, N, ED | None]]:
        assert node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        graph = self
        it = iter(self._node_outbound[node])
        class DummyIter:
            def __iter__(self):
                return self
            def __next__(self):
                while True:
                    e = next(it)
                    if predicate is None:
                        break
                    if predicate(*((e,) + graph.get_edge(e))):
                        break
                from_node, to_node, edge_data = graph.get_edge(e)
                return e, from_node, to_node, edge_data
        return DummyIter()

    def get_output_full(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> tuple[E, N, N, ED | None] | None:
        it = self.get_outputs_full(node, predicate)
        ret = next(it, None)
        after_ret = next(it, None)
        if after_ret is not None:
            raise ValueError('More than one edge exists')
        return ret

    def get_outputs(
            self: Graph,
            node: N,
            predicate: Callable[[E, ED | None], bool] | None = None
    ) -> Iterator[E]:
        assert node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        if predicate is None:
            return iter(self._node_outbound[node])
        else:
            return (e for e in self._node_outbound[node] if predicate(*((e,) + self.get_edge(e))))

    def get_output(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> E | None:
        it = self.get_outputs(node, predicate)
        ret = next(it, None)
        after_ret = next(it, None)
        if after_ret is not None:
            raise ValueError('More than one edge exists')
        return ret

    def has_outputs(
            self: Graph,
            node: N,
            predicate: Callable[[E, ED | None], bool] | None = None
    ) -> bool:
        assert node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        return next(self.get_outputs(node, predicate), None) is not None

    def get_degree(
            self: Graph,
            node: N,
            predicate: Callable[[E, ED | None], bool] | None = None
    ) -> int:
        assert node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        if predicate is None:
            return len(self._node_outbound[node])
        else:
            return sum(1 for e in self._node_outbound[node] if predicate(*((e,) + self.get_edge(e))))

    def copy(self: Graph) -> Graph[N, ND, E, ED]:
        copy_outbound = dict()
        for k, v in self._node_outbound.items():
            copy_outbound[k] = v.copy()
        graph = Graph()
        graph._node_outbound = copy_outbound
        graph._node_data = self._node_data.copy()
        graph._edges = self._edges.copy()
        return graph

    def to_directed_graph(self: Graph, root: N) -> DirectedGraph.Graph[N, ND, E, ED]:
        ret = DirectedGraph.Graph()
        for n in self.get_nodes():
            ret.insert_node(n, self.get_node_data(n))
        n_list = [root]
        n_walked = []
        while len(n_list) > 0:
            n_parent = n_list.pop()
            n_walked.append(n_parent)
            for e in self.get_outputs(n_parent):
                n1, n2, e_weight = self.get_edge(e)
                n_outputs = {n1, n2}
                n_outputs.remove(n_parent)
                n_child = n_outputs.pop()
                if n_child in n_walked:
                    continue
                ret.insert_edge(e, n_parent, n_child, e_weight)
                n_list.append(n_child)
        return ret

    def __len__(self: Graph) -> int:
        return len(self._node_outbound)

    def __contains__(self: Graph, item: N) -> bool:
        return item in self._node_outbound

    def __hash__(self: Graph) -> int:
        # don't bother including inbound because inbound and outbound are reflections of each other
        return hash((self._node_outbound, self._node_data, self._edges))

    def __eq__(self: Graph, o: Graph) -> bool:
        # don't bother including inbound because inbound and outbound are reflections of each other
        return type(self) == type(o) and\
               self._node_outbound == o._node_outbound and\
               self._node_data == o._node_data and\
               self._edges == o._edges

    def __str__(self: Graph) -> str:
        out = []
        walked_edges = set()
        for node, edges in self._node_outbound.items():
            for edge in edges:
                if edge in walked_edges:
                    continue
                walked_edges.add(edge)
                node1, node2, edge_data = self._edges[edge]
                line = f'({node1}'
                if self._node_data[node1] is not None:
                    line += f', {self._node_data[node1]}'
                line += f')--({edge}'
                if edge_data is not None:
                    line += f', {edge_data}'
                line += f')--({node2}'
                if self._node_data[node2] is not None:
                    line += f', {self._node_data[node2]}'
                line += f')'
                out.append(line)
            if len(edges) == 0:
                line = f'({node}'
                if self._node_data[node] is not None:
                    line += f', {self._node_data[node]}'
                line += f')--x'
                out.append(line)
        return '\n'.join(out)

    def __repr__(self: Graph) -> str:
        return str(self)


if __name__ == '__main__':
    g = Graph()
    g.insert_node('A')
    g.insert_node('B')
    g.insert_node('C')
    g.insert_node('D')
    g.insert_edge('AB1', 'A', 'B', 'MY EDGE DATA FOR 1st AB')
    g.insert_edge('AB2', 'A', 'B', 'MY EDGE DATA FOR 2nd AB')
    g.insert_edge('BC', 'B', 'C')
    g.insert_edge('CD', 'C', 'D')
    g.insert_edge('AD', 'A', 'D')
    g.insert_node('Z')
    print(f'{g}')
    print(f'{g.get_degree("A")}')
    print(f'{g.get_degree("B")}')
    print(f'{g.get_degree("C")}')
    print(f'{g.get_degree("D")}')
    g.insert_node('E')
    g.insert_edge('DE', 'D', 'E')
    print(f'{g}')
    g.delete_edge('AD')
    print(f'{g}')
    g.delete_edge('AC')  # error expected here
    print(f'{g}')
