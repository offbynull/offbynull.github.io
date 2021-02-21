from graph.Graph import Graph

with open('/home/user/Downloads/dataset_240312_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')

g = Graph()
for l in lines:
    text = l.strip().split(' -> ')
    in_node = text[0]
    out_nodes = text[1]
    for out_node in out_nodes.split(','):
        if not g.has_node(in_node):
            g.insert_node(in_node)
        if not g.has_node(out_node):
            g.insert_node(out_node)
        g.insert_edge(f'{in_node}->{out_node}', in_node, out_node)


topological_ordering = []
candidates = [n for n in g.get_nodes() if g.get_in_degree(n) == 0]  # Primed with root nodes
while len(candidates) != 0:
    node = candidates.pop(0)
    topological_ordering.append(node)
    for edge in list(g.get_outputs(node)):
        to_node = g.get_edge_to(edge)
        # Delete the edge. If the node it was pointing to no longer has any incoming edges (it is a root node now), add
        # it to candidates.
        g.delete_edge(edge)
        if not g.has_inputs(to_node):
            candidates.append(to_node)

print(f'{", ".join(topological_ordering)}')