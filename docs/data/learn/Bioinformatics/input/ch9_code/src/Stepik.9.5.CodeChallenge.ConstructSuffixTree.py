from graph.DirectedGraph import Graph
from graph.GraphHelpers import IntegerIdGenerator


def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' rankdir=LR\n'
    ret += ' node[fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        data = g.get_node_data(n)
        ret += f'{n} [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        ret += f'{n1} -> {n2} [label="{data}"]\n'
    ret += '}'
    return ret


def construct_suffix_tree(text: str):
    tree: Graph[int, None, int, str] = Graph()
    tree.insert_node(0)
    e_gen = IntegerIdGenerator(start_count=10000)
    n_gen = IntegerIdGenerator(start_count=1)
    for i in range(len(text) - 1, -1, -1):
        region = text[i:]
        cut_data = walk_to_cutpoint(tree, region)
        if cut_data[0] == 'EDGE':
            _, cut_e, cut_idx, remainder = cut_data
            cut_e_data = tree.get_edge_data(cut_e)
            new_n = n_gen.next_id()
            new_e1 = e_gen.next_id()
            new_e2 = e_gen.next_id()
            tree.insert_node_between_edge(
                new_n, None,
                cut_e,
                new_e1, cut_e_data[:cut_idx],
                new_e2, cut_e_data[cut_idx:]
            )
            n = new_n
        elif cut_data[0] == 'NODE':
            _, n, remainder = cut_data
        else:
            raise ValueError('This should never happen')
        new_n = n_gen.next_id()
        new_e = e_gen.next_id()
        tree.insert_node(new_n)
        tree.insert_edge(new_e, n, new_n, remainder)
        # print(region)
    return tree


def walk_to_cutpoint(tree: Graph[int, None, int, str], val: str):
    # Walk down edges
    n = tree.get_root_node()
    e = None
    consumed_len = -1
    while True:
        edge_full = tree.get_output_full(n, predicate=lambda e, n1, n2, ed: common_prefix_len(ed, val) > 0)
        # If no match found, leave
        if edge_full is None:
            break
        e, _, n2, ed = edge_full
        consumed_len = common_prefix_len(ed, val)
        # If partial match found, leave
        if consumed_len < len(ed):
            break
        n = n2
        val = val[consumed_len:]
    # On no edge match, the last node is where we need to extend from. Otherwise, we need to break the edge and extend
    # from there
    if edge_full is None:
        return 'NODE', n, val
    return 'EDGE', e, consumed_len, val[consumed_len:]


def common_prefix_len(s1: str, s2: str):
    l = min(len(s1), len(s2))
    count = 0
    for i in range(l):
        if s1[i] == s2[i]:
            count += 1
        else:
            break
    return count


with open('/home/user/Downloads/dataset_240378_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = data.strip().split('\n')
text = data[0]

# text = 'panamabananas$'
tree = construct_suffix_tree(text)
# print(f'{to_dot(tree)}')
edge_strs = [tree.get_edge_data(e) for e in tree.get_edges()]
print(' '.join(edge_strs))