from __future__ import annotations

from collections import Counter
from typing import TypeVar, Generic, Tuple, Iterator

T = TypeVar('T')


class Graph(Generic[T]):
    def __init__(self):
        self._outbound = dict()
        self._inbound = dict()

    def insert_node(self: Graph, node: T):
        assert node not in self._outbound  # if it's not in outbound, it won't be in inbound as well
        self._outbound[node] = Counter()
        self._inbound[node] = Counter()

    def replace_node(self: Graph, old_node: T, new_node: T):
        assert old_node in self._outbound  # if it's not in outbound, it won't be in inbound as well
        if new_node != old_node:
            assert new_node not in self._outbound  # if it's not in outbound, it won't be in inbound as well
        out_counter = self._outbound[old_node].copy()
        in_counter = self._inbound[old_node].copy()
        self.delete_node(old_node)
        self.insert_node(new_node)
        for to_node in out_counter.elements():
            self.insert_edge(new_node, to_node)
        for from_node in in_counter.elements():
            self.insert_edge(from_node, new_node)

    def delete_node(self: Graph, node: T):
        assert node in self._outbound
        for other_node in self._outbound[node].elements():
            count = self._inbound[other_node][node]
            count -= 1
            if count > 0:
                self._inbound[other_node][node] = count
            else:
                del self._inbound[other_node][node]
        for other_node in self._inbound[node].elements():
            count = self._outbound[other_node][node]
            count -= 1
            if count > 0:
                self._outbound[other_node][node] = count
            else:
                del self._outbound[other_node][node]
        del self._inbound[node]
        del self._outbound[node]

    def insert_edge(
            self: Graph,
            from_node: T,
            to_node: T,
            insert_from_if_not_exists: bool = True,
            insert_to_if_not_exists: bool = True):
        if insert_from_if_not_exists and from_node not in self._inbound:
            self.insert_node(from_node)
        else:
            assert from_node in self._outbound
        if insert_to_if_not_exists and to_node not in self._inbound:
            self.insert_node(to_node)
        else:
            assert to_node in self._outbound
        self._inbound[to_node][from_node] += 1
        self._outbound[from_node][to_node] += 1

    def delete_edge(
            self: Graph,
            from_node: T,
            to_node: T,
            remove_from_if_isolated: bool = False,
            remove_to_if_isolated: bool = False):
        assert from_node in self._outbound  # if it's in outbound, it'll be in inbound as well
        assert to_node in self._outbound  # if it's in outbound, it'll be in inbound as well
        count = self._outbound[from_node][to_node]
        assert count > 0
        count -= 1
        if count > 0:
            self._inbound[to_node][from_node] = count
            self._outbound[from_node][to_node] = count
        else:
            del self._inbound[to_node][from_node]
            del self._outbound[from_node][to_node]
        # from and to may be the same -- if they are, and you've removed the from, make sure you don't try to remove to
        # because form and to are the same... you can't remove the same node twice
        dealing_with_same_node = from_node == to_node
        removed_from = False
        removed_to = False
        if remove_from_if_isolated\
                and sum(self._inbound[from_node].values()) == 0\
                and sum(self._outbound[from_node].values()) == 0:
            self.delete_node(from_node)
            removed_from = True
        if remove_to_if_isolated \
                and (not dealing_with_same_node or (dealing_with_same_node and not removed_from))\
                and sum(self._inbound[to_node].values()) == 0\
                and sum(self._outbound[to_node].values()) == 0:
            self.delete_node(to_node)
            removed_to = True

    def get_nodes(self: Graph) -> Iterator[T]:
        return iter(self._outbound)

    def has_node(self: Graph, node: T) -> bool:
        return node in self._outbound  # inbound and outbound are reflections of each other, so only check one

    def get_all_outputs(self: Graph) -> Iterator[Tuple[T, Iterator[T]]]:
        return map(lambda i: (i[0], iter(i[1].elements())), self._outbound.items())

    def get_all_inputs(self: Graph) -> Iterator[Tuple[T, Iterator[T]]]:
        return map(lambda i: (i[0], iter(i[1].elements())), self._inbound.items())

    def get_outputs(self: Graph, node: T) -> Iterator[T]:
        assert node in self._outbound  # if it's in outbound, it'll be in inbound as well
        return iter(self._outbound[node].elements())

    def get_inputs(self: Graph, node: T) -> Iterator[T]:
        assert node in self._inbound  # if it's in inbound, it'll be in outbound as well
        return iter(self._inbound[node].elements())

    def has_outputs(self: Graph, node: T) -> Iterator[T]:
        assert node in self._outbound  # if it's in outbound, it'll be in inbound as well
        return next(self.get_outputs(node), None) is not None

    def has_inputs(self: Graph, node: T) -> Iterator[T]:
        assert node in self._inbound  # if it's in inbound, it'll be in outbound as well
        return next(self.get_inputs(node), None) is not None

    def get_out_degree(self: Graph, node: T) -> int:
        assert node in self._outbound  # if it's in outbound, it'll be in inbound as well
        return sum(self._outbound[node].values())

    def get_in_degree(self: Graph, node: T) -> int:
        assert node in self._inbound  # if it's in inbound, it'll be in outbound as well
        return sum(self._inbound[node].values())

    def copy(self: Graph) -> Graph[T]:
        copy_outbound = dict()
        for k, v in self._outbound.items():
            copy_outbound[k] = v.copy()
        copy_inbound = dict()
        for k, v in self._inbound.items():
            copy_inbound[k] = v.copy()
        graph = Graph()
        graph._outbound = copy_outbound
        graph._inbound = copy_inbound
        return graph

    def to_graphviz(self: Graph) -> str:
        out = ''
        for node, to_nodes in self._outbound.items():
            for to_node in to_nodes.elements():
                out += '"' + str(node).replace("\"", "\\\"") + '\"'\
                       + ' -> '\
                       + '"' + str(to_node).replace("\"", "\\\"") + '"'\
                       + ' [shape=plain];\n'
        return 'digraph {\n'\
               + 'graph[center=true, margin=0.2, nodesep=0.1, ranksep=0.2]\n'\
               + 'node[shape=none, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'\
               + 'edge[arrowsize=0.6, arrowhead=vee]\n'\
               + out\
               + '}\n'

    def __len__(self: Graph) -> int:
        return len(self._outbound)

    def __contains__(self: Graph, item: T) -> bool:
        return item in self._outbound

    def __hash__(self: Graph) -> int:
        # don't bother including inbound because inbound and outbound are reflections of each other
        return hash(self._outbound)

    def __eq__(self: Graph, o: Graph) -> bool:
        # don't bother including inbound because inbound and outbound are reflections of each other
        return type(self) == type(o) and self._outbound == o._outbound

    def __str__(self: Graph) -> str:
        out = []
        for node, to_nodes in self._outbound.items():
            out.append(f'{node}->[{",".join([str(e) for e in to_nodes.elements()])}]')
        return ', '.join(out)

    def __repr__(self: Graph) -> str:
        return str(self)


if __name__ == '__main__':
    g = Graph()
    g.insert_edge('A', 'B')
    g.insert_edge('B', 'C')
    g.insert_edge('C', 'D')
    g.insert_edge('A', 'D')
    print(f'{g}')
    print(f'{g.get_in_degree("A")} {g.get_out_degree("A")}')
    print(f'{g.get_in_degree("B")} {g.get_out_degree("B")}')
    print(f'{g.get_in_degree("C")} {g.get_out_degree("C")}')
    print(f'{g.get_in_degree("D")} {g.get_out_degree("D")}')
    g.insert_node('E')
    g.insert_edge('D', 'E')
    print(f'{g}')
    g.delete_edge('A', 'D')
    print(f'{g}')
    g.delete_edge('A', 'C')  # error expected here
    print(f'{g}')
