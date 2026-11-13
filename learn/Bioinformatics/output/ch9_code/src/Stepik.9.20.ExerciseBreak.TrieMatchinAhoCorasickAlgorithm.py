# Exercise Break: Construct all failure edges for the trie shown in the figure below.
#
# MY ANSWER
# --------
# I just implemented the algorithm. The entire trie with failure edges, with the exact same tree structure. That's why
# I didn't bother replicating it as ASCII. You can just generate the graph using the to_dot() with and without failure
# edges.

from collections import defaultdict

from graph.DirectedGraph import Graph

def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' node[fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        data = g.get_node_data(n)
        ret += f'{n} [label="{n}\\n{data}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        ret += f'{n1} -> {n2} [label="{data}"]\n'
    ret += '}'
    return ret












class FailureEdge:
    def __init__(self, skip_count: int):
        self.skip_count = skip_count

    def __str__(self):
        return f'SKIP{self.skip_count}'


def construct_trie(patterns: list[str]):
    tree = Graph()
    tree.insert_node(0, False)
    next_eid = 100000
    next_nid = 1
    # Generate standard trie edges
    for p in patterns:
        last_n = 0
        for i, ch in enumerate(p):
            e_list = tree.get_outputs(last_n)
            n_found = None
            for e in e_list:
                if tree.get_edge_data(e) == ch:
                    n_found = tree.get_edge_to(e)
                    break
            if n_found is None:
                tree.insert_node(next_nid, False)
                tree.insert_edge(next_eid, last_n, next_nid, ch)
                n_found = next_nid
                next_nid += 1
                next_eid += 1
            if i == len(p) - 1:
                tree.update_node_data(n_found, True)
            last_n = n_found
    # Generate failure edges
    for p in patterns:
        for i in range(2, len(p)):
            p_prefix = p[:i]
            n_from = walk_to_node(p_prefix, tree)
            p_prefix_trim = p_prefix[1:]
            n_to = walk_to_node(p_prefix_trim, tree)
            if n_to is None:
                continue
            fail_edge = tree.get_output_full(
                n_from,
                lambda e, n1, n2, e_data: n1 == n_from and n2 == n_to and isinstance(e_data, FailureEdge)
            )
            if fail_edge is not None:  # ensure existing edge is for what we were going to create anyway
                _, n_from_existing, n_to_existing, _ = fail_edge
                assert n_from == n_from_existing
                assert n_to == n_to_existing
                continue
            tree.insert_edge(next_eid, n_from, n_to, FailureEdge(i-1))
            next_eid += 1
    # Return
    return tree


def walk_to_node(text: str, tree: Graph):
    last_n = tree.get_root_node()
    found = True
    for ch in text:
        ch_found = False
        for _, _, n_to, e_data in tree.get_outputs_full(last_n):
            if ch == e_data:
                last_n = n_to
                ch_found = True
                break
        if not ch_found:
            found = False
            break
    return last_n if found else None


def trie_prefix_match(search_text: str, tree: Graph, start_node: str):
    n_last = start_node
    found = ''
    for i, ch in enumerate(search_text):
        # If at a leaf node, exit loop.
        if tree.get_out_degree(n_last) == 0:
            break
        # Does an edge exist for ch? If it does, pick travel down it for to the next iteration. Otherwise, exit loop.
        ch_edge = tree.get_output_full(
            n_last,
            predicate=lambda e, n1, n2, e_data: e_data == ch
        )
        if ch_edge is None:
            break
        _, _, n_to, _ = ch_edge
        n_last = n_to
        found += ch
    # If the ending node has an "end of text" marker, success.
    end_marker = tree.get_node_data(n_last) == True
    if end_marker:
        return found, 0, tree.get_root_node()
    # If the ending node has a failure edge, return its details so the next invocation can skip ahead to the node at the
    # end of that failure edge
    fail_edge = tree.get_output_full(
        n_last,
        lambda e, n1, n2, e_data: isinstance(e_data, FailureEdge)
    )
    if fail_edge is not None:
        _, _, to_n, fail_data = fail_edge
        return None, fail_data.skip_count, to_n
    # Otherwise, return that nothing was found (no skipping ahead.
    return None, 0, tree.get_root_node()



patterns = [
    'ananas',
    'and',
    'antenna',
    'banana',
    'bandana',
    'nab',
    'nana',
    'pan'
]
# text = 'bantenna'
# text = 'bananas'
# text = 'anana'

found_set = defaultdict(set)
tree = construct_trie(patterns)
print(f'{to_dot(tree)}')


n = tree.get_root_node()
skip_count = 0
while text != '':
    skipped_text = text[skip_count:]
    found_prefix_skip = text[:skip_count]
    found_suffix, skip_count, n = trie_prefix_match(skipped_text, tree, n)
    if found_suffix is None:
        print(f'MOVING PAST {text[0]}', end='')
        if skip_count != 0:
            print(f', PREFIX FOUND {text[1:1+skip_count]}', end='')
        print()
        text = text[1:]
        continue
    found = found_prefix_skip + found_suffix
    print(f'FOUND {found}')
    text = text[len(found):]
print('FINISHED!')