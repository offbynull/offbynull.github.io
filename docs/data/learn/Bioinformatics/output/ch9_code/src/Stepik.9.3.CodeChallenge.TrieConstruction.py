from graph import DirectedGraph

with open('/home/user/Downloads/dataset_240376_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
patterns = data.strip().split(' ')

tree = DirectedGraph.Graph()
tree.insert_node(0, False)
next_eid = 100000
next_nid = 1
for p in patterns:
    last_nid = 0
    for i, ch in enumerate(p):
        e_list = tree.get_outputs(last_nid)
        found_nid = None
        for e in e_list:
            if tree.get_edge_data(e) == ch:
                found_nid = tree.get_edge_to(e)
                break
        if found_nid is None:
            tree.insert_node(next_nid)
            tree.insert_edge(next_eid, last_nid, next_nid, ch)
            found_nid = next_nid
            next_nid += 1
            next_eid += 1
        if i == len(p) - 1:
            tree.update_node_data(found_nid, True)
        last_nid = found_nid

for e in tree.get_edges():
    print(f'{tree.get_edge_from(e)} {tree.get_edge_to(e)} {tree.get_edge_data(e)}')