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







class EdgeData:
    def __init__(self, text: str, count: int):
        self.text = text
        self.count = count

    def __str__(self):
        return f'{(self.text, self.count)}'





def construct_suffix_tree(text: str):
    tree: Graph[int, None, int, EdgeData] = Graph()
    tree.insert_node(0)
    e_gen = IntegerIdGenerator(start_count=10000)
    n_gen = IntegerIdGenerator(start_count=1)
    for i in range(len(text) - 1, -1, -1):
        region = text[i:]
        cutpoint = walk_to_cutpoint(tree, region)
        # For any edge traversed to the cut point, the region traverse it over it again, so increment counts
        for e in cutpoint.e_list:
            tree.get_edge_data(e).count += 1
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
                new_e1, EdgeData(cut_e_data.text[:cut_idx], cut_e_data.count),
                new_e2, EdgeData(cut_e_data.text[cut_idx:], 1)
            )
            n = new_n
        elif isinstance(cutpoint, NodeCutpoint):
            n = cutpoint.n
            inject = cutpoint.inject_str
        else:
            raise ValueError('This should never happen')
        new_n = n_gen.next_id()
        new_e = e_gen.next_id()
        tree.insert_node(new_n)
        tree.insert_edge(new_e, n, new_n, EdgeData(inject, 1))
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


def walk_to_cutpoint(tree: Graph[int, None, int, EdgeData], val: str):
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


def walk_as_long_as_count_more_than_1(tree: Graph[int, None, int, EdgeData], n: int, prev_str: str):
    for e in tree.get_outputs(n):
        e_data = tree.get_edge_data(e)
        if e_data.count < 2:
            continue
        next_n = tree.get_edge_to(e)
        next_str = prev_str + e_data.text
        yield next_str
        yield from walk_as_long_as_count_more_than_1(tree, next_n, next_str)


def longest_repeat(tree: Graph[int, None, int, EdgeData], end_marker: str = '$'):
    # Walk the tree depth-first -- everything up until a branch
    root = tree.get_root_node()
    found = ''
    for text in walk_as_long_as_count_more_than_1(tree, root, ''):
        # Strip off end marker if it exists?
        if text.endswith(end_marker):
            text = text[:-len(end_marker)]
        # Keep it if it's the longest seen so far
        if len(text) > len(found):
            found = text
    return found




# NOTE: The strings provided here aren't adding in a special "end marker" at the end of the string like it did for the
# previous code challenge. The end marker is explictly being added here as '$'.
with open('/home/user/Downloads/dataset_240378_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = data.strip().split('\n')
text = data[0]
# text = 'ABCDEFG'
text += '$'  # add a special marker at the end because this exercise doesn't provide it
tree = construct_suffix_tree(text)
# print(f'{to_dot(tree)}')
print(f'{longest_repeat(tree, "$")}')


