from __future__ import annotations

from typing import TypeVar, Generic, Tuple, Iterator, Optional, Callable

# Adapted from the graph class I built to solve chapter 3 problems (genome assembly)
from graph import UndirectedGraph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')


class Graph(Generic[N, ND, E, ED]):
    def __init__(self):
        self._node_outbound = {}
        self._node_inbound = {}
        self._node_data = {}
        self._edges = {}

    def insert_node(self: Graph, node: N, data: Optional[ND] = None):
        assert node not in self._node_outbound  # if it's not in outbound, it won't be in inbound as well
        self._node_outbound[node] = set()
        self._node_inbound[node] = set()
        self._node_data[node] = data

    def delete_node(self: Graph, node: N):
        assert node in self._node_outbound
        for edge_id in self._node_outbound[node].copy():
            from_node, to_node, _ = self._edges[edge_id]
            self._node_outbound[from_node].remove(edge_id)
            self._node_inbound[to_node].remove(edge_id)
            del self._edges[edge_id]
        for edge_id in self._node_inbound[node].copy():
            from_node, to_node, _ = self._edges[edge_id]
            self._node_outbound[from_node].remove(edge_id)
            self._node_inbound[to_node].remove(edge_id)
            del self._edges[edge_id]
        del self._node_inbound[node]
        del self._node_outbound[node]
        del self._node_data[node]

    def update_node_data(self: Graph, node: N, data: Optional[ND] = None):
        assert node in self._node_outbound  # if it's not in outbound, it won't be in inbound as well
        self._node_data[node] = data

    def get_node_data(self: Graph, node: N) -> Optional[ND]:
        assert node in self._node_outbound
        return self._node_data[node]

    def insert_node_between_edge(
            self: Graph,
            new_node: N,
            new_node_data: ND | None,
            existing_edge: E,
            from_edge: E,
            from_edge_data: ED | None,
            to_edge: E,
            to_edge_data: ED | None
    ):
        assert new_node not in self._node_outbound
        assert existing_edge in self._edges
        assert from_edge not in self._edges
        assert to_edge not in self._edges
        node_from, node_to, _ = self.get_edge(existing_edge)
        self.insert_node(new_node, new_node_data)
        self.delete_edge(existing_edge)
        self.insert_edge(from_edge, node_from, new_node, from_edge_data)
        self.insert_edge(to_edge, new_node, node_to, to_edge_data)

    def insert_edge(
            self: Graph,
            edge: E,
            from_node: N,
            to_node: N,
            data: Optional[ED] = None):
        assert from_node in self._node_outbound
        assert to_node in self._node_outbound
        assert edge not in self._edges
        self._edges[edge] = (from_node, to_node, data)
        self._node_inbound[to_node].add(edge)
        self._node_outbound[from_node].add(edge)

    def delete_edge(
            self: Graph,
            edge: E,
            remove_from_if_isolated: bool = False,
            remove_to_if_isolated: bool = False):
        assert edge in self._edges
        from_node, to_node, _ = self._edges[edge]
        assert from_node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        assert to_node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        self._node_outbound[from_node].remove(edge)
        self._node_inbound[to_node].remove(edge)
        # from and to may be the same -- if they are, and you've removed the from, make sure you don't try to remove to
        # because form and to are the same... you can't remove the same node twice
        dealing_with_same_node = from_node == to_node
        removed_from = False
        removed_to = False
        if remove_from_if_isolated\
                and len(self._node_inbound[from_node]) == 0\
                and len(self._node_outbound[from_node]) == 0:
            self.delete_node(from_node)
            removed_from = True
        if remove_to_if_isolated \
                and (not dealing_with_same_node or (dealing_with_same_node and not removed_from))\
                and len(self._node_inbound[to_node]) == 0\
                and len(self._node_outbound[to_node]) == 0:
            self.delete_node(to_node)
            removed_to = True
        del self._edges[edge]

    # updates the data for the FIRST edge b
    def update_edge_data(
            self: Graph,
            edge: E,
            data: Optional[ED] = None):
        from_node, to_node, _ = self._edges[edge]
        self.delete_edge(edge)
        self.insert_edge(edge, from_node, to_node, data)

    def get_edge_data(self: Graph, edge: E) -> Optional[ED]:
        return self._edges[edge][2]

    def get_edge_from(self: Graph, edge: E) -> N:
        return self._edges[edge][0]

    def get_edge_to(self: Graph, edge: E) -> N:
        return self._edges[edge][1]

    def get_edge(self: Graph, edge: E) -> tuple[N, N, ED]:
        return self._edges[edge]

    def get_root_nodes(self: Graph) -> Iterator[N]:
        return (n for n in self.get_nodes() if self.get_in_degree(n) == 0)

    def get_root_node(self: Graph) -> N:
        roots = list(self.get_root_nodes())
        if len(roots) != 1:
            raise ValueError(f'Exactly 1 root node required: {roots}')
        return roots[0]

    def get_leaf_nodes(self: Graph) -> Iterator[N]:
        return (n for n in self.get_nodes() if self.get_out_degree(n) == 0)

    def get_leaf_node(self: Graph) -> N:
        leaves = list(self.get_leaf_nodes())
        if len(leaves) != 1:
            raise ValueError(f'Exactly 1 leaf node required: {leaves}')
        return leaves[0]

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
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
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

    def get_inputs_full(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> Iterator[tuple[E, N, N, ED | None]]:
        assert node in self._node_inbound  # if it's in inbound, it'll be in outbound as well
        graph = self
        it = iter(self._node_inbound[node])
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

    def get_input_full(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> tuple[E, N, N, ED | None] | None:
        it = self.get_inputs_full(node, predicate)
        ret = next(it, None)
        after_ret = next(it, None)
        if after_ret is not None:
            raise ValueError('More than one edge exists')
        return ret

    def get_outputs(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
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

    def get_inputs(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> Iterator[E]:
        assert node in self._node_inbound  # if it's in inbound, it'll be in outbound as well
        if predicate is None:
            return iter(self._node_inbound[node])
        else:
            return (e for e in self._node_inbound[node] if predicate(*((e,) + self.get_edge(e))))

    def get_input(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> E | None:
        it = self.get_inputs(node, predicate)
        ret = next(it, None)
        after_ret = next(it, None)
        if after_ret is not None:
            raise ValueError('More than one edge exists')
        return ret

    def has_outputs(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> bool:
        assert node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        return next(self.get_outputs(node, predicate), None) is not None

    def has_inputs(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> bool:
        assert node in self._node_inbound  # if it's in inbound, it'll be in outbound as well
        return next(self.get_inputs(node, predicate), None) is not None

    def get_out_degree(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> int:
        assert node in self._node_outbound  # if it's in outbound, it'll be in inbound as well
        if predicate is None:
            return len(self._node_outbound[node])
        else:
            return sum(1 for e in self._node_outbound[node] if predicate(*((e,) + self.get_edge(e))))

    def get_in_degree(
            self: Graph,
            node: N,
            predicate: Callable[[E, N, N, ED | None], bool] | None = None
    ) -> int:
        assert node in self._node_inbound  # if it's in inbound, it'll be in outbound as well
        if predicate is None:
            return len(self._node_inbound[node])
        else:
            return sum(1 for e in self._node_inbound[node] if predicate(*((e,) + self.get_edge(e))))

    def copy(self: Graph) -> Graph[N, ND, E, ED]:
        copy_outbound = dict()
        for k, v in self._node_outbound.items():
            copy_outbound[k] = v.copy()
        copy_inbound = dict()
        for k, v in self._node_inbound.items():
            copy_inbound[k] = v.copy()
        graph = Graph()
        graph._node_outbound = copy_outbound
        graph._node_inbound = copy_inbound
        graph._node_data = self._node_data.copy()
        graph._edges = self._edges.copy()
        return graph

    def to_undirected_graph(self: Graph) -> UndirectedGraph.Graph[N, ND, E, ED]:
        ret = UndirectedGraph.Graph()
        for n in self.get_nodes():
            ret.insert_node(n, self.get_node_data(n))
        for e in self.get_edges():
            ret.insert_edge(e, self.get_edge_from(e), self.get_edge_to(e), self.get_edge_data(e))
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
        for node, edges in self._node_outbound.items():
            for edge in edges:
                from_node, to_node, edge_data = self._edges[edge];
                out.append(f'{(from_node, self._node_data[from_node])}--'
                           f'{(edge, edge_data)}->'
                           f'{(to_node, self._node_data[to_node])}')
            if len(edges) == 0:
                out.append(f'{(node, self._node_data[node])}--x')
        return '\n'.join(out)

    def __repr__(self: Graph) -> str:
        return str(self)
#
#
# if __name__ == '__main__':
#     g = Graph()
#     g.insert_node('A')
#     g.insert_node('B')
#     g.insert_node('C')
#     g.insert_node('D')
#     g.insert_edge('A', 'B', 'MY EDGE DATA FOR 1st AB')
#     g.insert_edge('A', 'B', 'MY EDGE DATA FOR 2nd AB')
#     g.insert_edge('B', 'C')
#     g.insert_edge('C', 'D')
#     g.insert_edge('A', 'D')
#     print(f'{g}')
#     print(f'{g.get_in_degree("A")} {g.get_out_degree("A")}')
#     print(f'{g.get_in_degree("B")} {g.get_out_degree("B")}')
#     print(f'{g.get_in_degree("C")} {g.get_out_degree("C")}')
#     print(f'{g.get_in_degree("D")} {g.get_out_degree("D")}')
#     g.insert_node('E')
#     g.insert_edge('D', 'E')
#     print(f'{g}')
#     g.delete_edge('A', 'D')
#     print(f'{g}')
#     g.delete_edge('A', 'C')  # error expected here
#     print(f'{g}')
