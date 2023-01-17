from __future__ import annotations
import random

from gephistreamer import streamer, graph

# Install Gephi 0.9.6, install the GephiStream plugin, then create a new project and in "Streaming" panel (next to the
# "Layout" panel) set it to listen on port 8999 and start the server.


class GephiGraph:
    def __init__(self):
        self._stream = None
        self._ws_stream = None
        self._nodes = {}
        self._edges = {}

    def __enter__(self):
        self._ws_stream = streamer.GephiWS(hostname='localhost', port=8999, workspace='workspace1')
        self._stream = streamer.Streamer(self._ws_stream, auto_commit=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._ws_stream is None:
            return
        try:
            self._ws_stream.websocket.close()
        except RuntimeError:
            ...  # Do nothing
        self._ws_stream = None
        self._stream = None

    def new_node(self, node_id: str):
        if node_id in self._nodes:
            raise ValueError()
        n = graph.Node(node_id)
        n.property['x'] = random.random() * 50.0
        n.property['y'] = random.random() * 50.0
        n.property['z'] = 0.0
        self._stream.add_node(n)
        n = graph.Node(node_id)  # Create new node so as to not have xyz set on the node (messes up Gephi layouts algos)
        del n.property['x']
        del n.property['y']
        del n.property['z']
        ret = GephiGraphNode(node_id, self, n)
        self._nodes[node_id] = ret
        return ret

    def new_edge(self, from_node_id: str, to_node_id: str):
        if from_node_id not in self._nodes:
            self.new_node(from_node_id)
        if to_node_id not in self._nodes:
            self.new_node(to_node_id)
        if (from_node_id, to_node_id) in self._edges:
            raise ValueError()
        e = graph.Edge(from_node_id, to_node_id)
        self._stream.add_edge(e)
        ret = GephiGraphEdge((from_node_id, to_node_id), self, e)
        self._edges[from_node_id, to_node_id] = ret
        return ret

    def get_node(self, node_id: str) -> GephiGraphNode:
        return self._nodes[node_id]

    def get_edge(self, from_node_id: str, to_node_id: str) -> GephiGraphEdge:
        return self._edges[from_node_id, to_node_id]

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    def has_edge(self, from_node_id: str, to_node_id: str) -> bool:
        return (from_node_id, to_node_id) in self._edges

    def commit(self):
        self._stream.commit()


class GephiGraphNode:
    def __init__(self, id: str, gg: GephiGraph, node: graph.Node):
        self._id = id
        self._gg = gg
        self._node = node

    def update_size(self, size: float):
        if self._node.property.get('Size', None) != size:
            self._node.property['Size'] = size
            self._gg._stream.change_node(self._node)

    def update_color(self, r: float, g: float, b: float):
        if (r, g, b) != (self._node.property.get('r', None), self._node.property.get('g', None), self._node.property.get('b', None)):
            self._node.property['r'] = r
            self._node.property['g'] = g
            self._node.property['b'] = b
            self._gg._stream.change_node(self._node)

    def delete(self):
        self._gg._stream_.delete_node(self._node)
        del self._gg._stream_.nodes[self._id]
        self._gg = None


class GephiGraphEdge:
    def __init__(self, id: tuple[str, str], gg: GephiGraph, edge: graph.Edge):
        self._id = id
        self._gg = gg
        self._edge = edge

    def update_weight(self, size: float):
        if self._edge.property.get('Weight', None) != size:
            self._edge.property['Weight'] = size
            self._gg._stream.change_edge(self._edge)

    def update_color(self, r: float, g: float, b: float):
        if (r, g, b) != (self._edge.property.get('r', None), self._edge.property.get('g', None), self._edge.property.get('b', None)):
            self._edge.property['r'] = r
            self._edge.property['g'] = g
            self._edge.property['b'] = b
            self._gg._stream.change_edge(self._edge)

    def delete(self):
        self._gg._stream_.delete_edge(self._edge)
        del self._gg._stream_.delete_edge[self._id]
        self._gg = None


if __name__ == '__main__':
    with GephiGraph() as gg:
        n1 = gg.new_node('Apple')
        n2 = gg.new_node('Banana')
        e1 = gg.new_edge('Apple', 'Banana')
        n2.update_size(2.5)
        n2.update_color(1.0, 0.0, 0.0)
        gg.commit()
        n3 = gg.new_node('Orange')
        e2 = gg.new_edge('Apple', 'Orange')
        e3 = gg.new_edge('Apple', 'Avocado')
        gg.commit()
