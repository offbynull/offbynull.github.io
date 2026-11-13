from collections import Counter

from graph.DirectedGraph import Graph
from graph.GraphHelpers import IntegerIdGenerator



def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' rankdir=LR\n'
    ret += ' node[fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        data = g.get_node_data(n)
        ret += f'{n} [style=filled fillcolor={data} label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        ret += f'{n1} -> {n2} [label="{data}"]\n'
    ret += '}'
    return ret







class EdgeData:
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return f'{self.text}'





def construct_suffix_tree(text: str):
    tree: Graph[int, str, int, EdgeData] = Graph()
    tree.insert_node(0, '?')
    e_gen = IntegerIdGenerator(start_count=10000)
    n_gen = IntegerIdGenerator(start_count=1)
    for i in range(len(text) - 1, -1, -1):
        region = text[i:]
        cutpoint = walk_to_cutpoint(tree, region)
        if isinstance(cutpoint, EdgeCutpoint):
            cut_e = cutpoint.e
            cut_idx = cutpoint.cut_index
            inject = cutpoint.inject_str
            cut_e_data = tree.get_edge_data(cut_e)
            # Inject a node inbetween the edge at the cut location, but the new edge that branches off (the one for
            # that's unique for the tail of region) must have a count of 1.
            new_n = n_gen.next_id()
            new_e1 = e_gen.next_id()
            new_e2 = e_gen.next_id()
            tree.insert_node_between_edge(
                new_n, None,
                cut_e,
                new_e1, EdgeData(cut_e_data.text[:cut_idx]),
                new_e2, EdgeData(cut_e_data.text[cut_idx:])
            )
            n = new_n
        elif isinstance(cutpoint, NodeCutpoint):
            n = cutpoint.n
            inject = cutpoint.inject_str
        else:
            raise ValueError('This should never happen')
        new_n = n_gen.next_id()
        new_e = e_gen.next_id()
        tree.insert_node(new_n, '?')
        tree.insert_edge(new_e, n, new_n, EdgeData(inject))
    return tree


class NodeCutpoint:
    def __init__(self, n: int, inject_str: str, e_list: list[int]):
        self.n = n
        self.inject_str = inject_str
        self.e_list = e_list


class EdgeCutpoint:
    def __init__(self, e: int, cut_index, inject_str, e_list: list[int]):
        self.e = e
        self.cut_index = cut_index
        self.inject_str = inject_str
        self.e_list = e_list


def walk_to_cutpoint(tree: Graph[int, str, int, EdgeData], val: str):
    e_list = []
    # Walk down edges
    n = tree.get_root_node()
    e = None
    consumed_len = -1
    while True:
        edge_full = tree.get_output_full(n, predicate=lambda e, n1, n2, ed: common_prefix_len(ed.text, val) > 0)
        # If no match found, leave
        if edge_full is None:
            break
        e, _, n2, ed = edge_full
        e_list.append(e)
        consumed_len = common_prefix_len(ed.text, val)
        # If partial match found, leave
        if consumed_len < len(ed.text):
            break
        n = n2
        val = val[consumed_len:]
    # On no edge match, the last node is where we need to extend from. Otherwise, we need to break the edge and extend
    # from there
    if edge_full is None:
        return NodeCutpoint(n, val, e_list)
    return EdgeCutpoint(e, consumed_len, val[consumed_len:], e_list)


def common_prefix_len(s1: str, s2: str):
    l = min(len(s1), len(s2))
    count = 0
    for i in range(l):
        if s1[i] == s2[i]:
            count += 1
        else:
            break
    return count


def walk_until_non_purple(tree: Graph[int, str, int, EdgeData], n: int, stop_color: str, prev_str: str):
    assert tree.get_node_data(n) == 'purple'
    for e in tree.get_outputs(n):
        e_data = tree.get_edge_data(e)
        next_n = tree.get_edge_to(e)
        if tree.get_node_data(next_n) == stop_color:
            yield prev_str, e_data.text
        if tree.get_node_data(next_n) != 'purple':
            continue
        next_str = prev_str + e_data.text
        yield from walk_until_non_purple(tree, next_n, stop_color, next_str)


def shortest_non_repeat(tree: Graph[int, str, int, EdgeData], stop_color: str, end_markers: set[str]):
    root = tree.get_root_node()
    found = ''
    for purple_text, to_non_purple_text in walk_until_non_purple(tree, root, stop_color, ''):
        next_ch = to_non_purple_text[0]
        if next_ch in end_markers:
            continue
        text = purple_text + next_ch
        if found == '' or len(text) < len(found):
            found = text
    return found


def color_tree_leaves(tree: Graph[int, str, int, EdgeData], text1Len: int, text2Len: int):
    for n in set(tree.get_leaf_nodes()):
        _, _, _, ed = tree.get_input_full(n)
        if len(ed.text) <= text1Len:
            tree.update_node_data(n, 'blue')
        else:
            tree.update_node_data(n, 'red')


def color_tree_internal(tree: Graph[int, str, int, EdgeData]):
    remaining = Counter({n: tree.get_out_degree(n) for n in tree.get_nodes()})
    for n in tree.get_leaf_nodes():
        _, parent_n, _, _ = tree.get_input_full(n)
        remaining[parent_n] -= 1
        remaining.pop(n)
    while len(remaining) > 0:
        n = next(n for n, count in remaining.items() if count == 0)
        if tree.has_inputs(n):
            _, parent_n, _, _ = tree.get_input_full(n)
            remaining[parent_n] -= 1
        remaining.pop(n)
        child_colors = set(tree.get_node_data(c_n) for _, _, c_n, _ in tree.get_outputs_full(n))
        if child_colors == {'red'}:
            tree.update_node_data(n, 'red')
        elif child_colors == {'blue'}:
            tree.update_node_data(n, 'blue')
        else:
            tree.update_node_data(n, 'purple')




with open('/home/user/Downloads/dataset_240378_7.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
text1 = data[0] + '#'
text2 = data[1] + '$'
tree = construct_suffix_tree(text1 + text2)
color_tree_leaves(tree, len(text1), len(text2))
color_tree_internal(tree)
# print(f'{to_dot(tree)}')
print(f'{shortest_non_repeat(tree, "red", {"#", "$"})}')


