from collections import defaultdict

from graph.DirectedGraph import Graph


def construct_trie(patterns: list[str]):
    tree = Graph()
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
    return tree


def trie_prefix_match(text: str, tree: Graph[int, str, int, bool]):
    last_nid = next(n for n in tree.get_nodes() if tree.get_in_degree(n) == 0)  # root
    ret = ''
    found = False
    for ch in text:
        if tree.get_out_degree(last_nid) == 0:
            found = True
            break
        ch_found = False
        for e in tree.get_outputs(last_nid):
            if ch == tree.get_edge_data(e):
                last_nid = tree.get_edge_to(e)
                ret += ch
                ch_found = True
                break
        if not ch_found:
            found = False
            break
    return ret if found else None



with open('/home/user/Downloads/dataset_240376_8.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = data.strip().split('\n')
text = data[0]
patterns = data[1].strip().split(' ')

found_set = defaultdict(set)
tree = construct_trie(patterns)
for i, _ in enumerate(text):
    found = trie_prefix_match(text[i:], tree)
    if found is not None:
        found_set[found].add(i)

for found, idxes in found_set.items():
    print(f'{found}: {" ".join(str(i) for i in idxes)}')