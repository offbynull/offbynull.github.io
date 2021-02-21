from graph.Graph import Graph

g = Graph()
g.insert_node('n0', -1)
g.insert_node('n1', -1)
g.insert_node('n2', -1)
g.insert_node('n3', -1)
g.insert_node('n4', -1)
g.insert_node('n5', -1)
g.insert_node('n6', -1)
g.insert_node('n7', -1)
g.insert_edge('e0', 'n0', 'n1', 2)
g.insert_edge('e1', 'n0', 'n3', 4)
g.insert_edge('e2', 'n1', 'n4', 5)
g.insert_edge('e3', 'n1', 'n5', 1)
g.insert_edge('e4', 'n1', 'n6', 3)
g.insert_edge('e5', 'n2', 'n0', 1)
g.insert_edge('e6', 'n2', 'n3', 3)
g.insert_edge('e7', 'n3', 'n5', 3)
g.insert_edge('e8', 'n3', 'n7', 7)
g.insert_edge('e9', 'n4', 'n3', 2)
g.insert_edge('ea', 'n4', 'n5', 8)
g.insert_edge('eb', 'n5', 'n6', 3)
g.insert_edge('ec', 'n5', 'n7', 2)
g.insert_edge('ed', 'n7', 'n6', 2)

check_nodes = set()
ready_nodes = set()
for n in g.get_nodes():
    if g.get_in_degree(n) == 0:
        g.update_node_data(n, 0)
        check_nodes |= {g.get_edge_to(e) for e in g.get_outputs(n)}
        ready_nodes |= {n}

while len(check_nodes) > 0:
    for n in check_nodes:
        incoming_nodes = {g.get_edge_from(e) for e in g.get_inputs(n)}
        if incoming_nodes.issubset(ready_nodes):
            accum_weight_from_each_incoming_node = [g.get_node_data(g.get_edge_from(e)) + g.get_edge_data(e) for e in g.get_inputs(n)]
            n_weight = max(accum_weight_from_each_incoming_node)
            g.update_node_data(n, n_weight)
            check_nodes.remove(n)
            check_nodes |= {g.get_edge_to(e) for e in g.get_outputs(n)}
            ready_nodes |= {n}
            break


print(f'{g.get_node_data("n6")}')
