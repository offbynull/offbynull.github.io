# Challenge Problem: Construct the evolutionary tree for a different HIV protein. Does this tree also support conviction
# of Dr. Schmidt? Reconstruct the ancestral HIV sequences at the internal nodes of the resulting trees.
#
#
# ANSWER: This is exactly the same thing as Stepik.7.10.ExerciseBreak.AlignmentToEvolutionaryTree.py, just with
# different sequences.

import math
import textwrap
from collections import Counter
from itertools import product

from distance_matrix.DistanceMatrix import DistanceMatrix
from graph import UndirectedGraph, DirectedGraph
from phylogeny.NeighbourJoiningPhylogeny import neighbour_joining_phylogeny

def to_dot(g_list: list[DirectedGraph.Graph], seqs: dict[str, str]) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=TB]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g_list[0].get_nodes())
    for n in nodes:
        if n.startswith('_INTERNAL'):
            ret += f'{n} [label="{n}\n{"".join(g.get_node_data(n).element for g in g_list[:25])}..."]\n'
        else:
            ret += f'{n} [label="{[k for k, v in seqs.items() if v == n].pop()}\n{n[:25]}..."]\n'
    for e in sorted(g_list[0].get_edges()):
        n1, n2, weight = g_list[0].get_edge(e)
        ret += f'{n1} -- {n2} [label="{sum(g.get_edge_data(e).hamming_distance for g in g_list)}"]\n'
    ret += '}'
    return ret

class NodeData:
    def __init__(self, element: str):
        self.element = element
        self.alphabet_scores = {ch: math.nan for ch in 'GASPVTCILNDKQEMHFRYWX'}
        assert element == '?' or element in self.alphabet_scores.keys(), f'Bad element? {element}'
        self.tagged = False

    def set_score(self, alphabet_elem: str, score: float):
        self.alphabet_scores[alphabet_elem] = score

    def get_score(self, alphabet_elem: str):
        return self.alphabet_scores[alphabet_elem]

    def resolve_element(self, p_element: str):
        # you can technically pick any minimum, but if you want to match the sample output you need to make it so that
        # it tries to tiebreak by looking at the parent's element (submitted here as p_element)
        min_score = min(self.alphabet_scores.values())
        possibilities = {k for k, v in self.alphabet_scores.items() if v == min_score}
        if p_element in possibilities:
            self.element = p_element
        else:
            self.element = possibilities.pop()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class EdgeData:
    def __init__(self):
        self.hamming_distance = math.inf

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


def alpha(symbol1: str, symbol2: str):
    if symbol1 == symbol2:
        return 0
    else:
        return 1


def compute_internal_node_score(tree: DirectedGraph.Graph[str, NodeData, str, EdgeData], n: str):
    n_ch1, n_ch2 = tuple(tree.get_edge_to(e) for e in tree.get_outputs(n))
    n_data = tree.get_node_data(n)
    n_ch1_data = tree.get_node_data(n_ch1)
    n_ch2_data = tree.get_node_data(n_ch2)
    for s in 'GASPVTCILNDKQEMHFRYWX':
        ch1_min = min(n_ch1_data.get_score(_s) + alpha(s, _s) for _s in 'GASPVTCILNDKQEMHFRYWX')
        ch2_min = min(n_ch2_data.get_score(_s) + alpha(s, _s) for _s in 'GASPVTCILNDKQEMHFRYWX')
        n_data.set_score(s, ch1_min + ch2_min)


def small_parsimony(tree: DirectedGraph.Graph[str, NodeData, str, EdgeData]):
    for n in tree.get_nodes():
        n_data = tree.get_node_data(n)
        n_data.tagged = False
        if not n.startswith('_INTERNAL'):  # is leaf node
            n_data.tagged = True
            for e in 'GASPVTCILNDKQEMHFRYWX':
                if n_data.element == e:
                    n_data.set_score(e, 0.0)
                else:
                    n_data.set_score(e, math.inf)
    nodes_untagged_but_all_children_tagged = Counter()
    for n in tree.get_nodes():
        if not n.startswith('_INTERNAL'):
            continue  # don't include leaf nodes
        nodes_untagged_but_all_children_tagged[n] = tree.get_out_degree(n)
        for e in tree.get_outputs(n):
            n_child = tree.get_edge_to(e)
            if tree.get_node_data(n_child).tagged:
                nodes_untagged_but_all_children_tagged[n] -= 1
    while len(nodes_untagged_but_all_children_tagged) > 0:
        ripe_nodes = [n for n, c in nodes_untagged_but_all_children_tagged.items() if c == 0]
        n = ripe_nodes.pop()
        n_data = tree.get_node_data(n)
        n_data.tagged = True
        compute_internal_node_score(tree, n)
        del nodes_untagged_but_all_children_tagged[n]
        for e in tree.get_inputs(n):
            p = tree.get_edge_from(e)
            nodes_untagged_but_all_children_tagged[p] -= 1


def backtrack_to_create_elements_and_weights(tree: DirectedGraph.Graph[str, NodeData, str, EdgeData]):
    root_n = [n for n in tree.get_nodes() if tree.get_in_degree(n) == 0].pop()
    root_n_data = tree.get_node_data(root_n)
    root_n_data.resolve_element('')
    pending = [root_n]
    while pending:
        n = pending.pop()
        for e in tree.get_outputs(n):
            n_from, n_to, e_data = tree.get_edge(e)
            n_from_data = tree.get_node_data(n_from)
            n_to_data = tree.get_node_data(n_to)
            n_to_data.resolve_element(n_from_data.element)
            elem_from = tree.get_node_data(n).element
            elem_to = tree.get_node_data(n_to).element
            e_data.hamming_distance = 0 if elem_from == elem_to else 1
            pending.append(n_to)


def nn_swap(edge_id: str, t_per_idx: list[UndirectedGraph.Graph]):
    n1, n2, _ = t_per_idx[0].get_edge(edge_id)
    n1_edge_ids = [e for e in t_per_idx[0].get_outputs(n1) if e != edge_id]
    n2_edge_ids = [e for e in t_per_idx[0].get_outputs(n2) if e != edge_id]
    n1_1, n1_2 = [_n for e in n1_edge_ids for _n in t_per_idx[0].get_edge_ends(e) if _n != n1]
    n2_1, n2_2 = [_n for e in n2_edge_ids for _n in t_per_idx[0].get_edge_ends(e) if _n != n2]
    t1_per_idx = []
    t2_per_idx = []
    for _t in t_per_idx:
        t1 = _t.copy()
        t1.delete_edge(n1_edge_ids[0])
        t1.delete_edge(n1_edge_ids[1])
        t1.delete_edge(n2_edge_ids[0])
        t1.delete_edge(n2_edge_ids[1])
        t1.insert_edge(n1_edge_ids[0], n1, n1_1)
        t1.insert_edge(n1_edge_ids[1], n1, n2_1)
        t1.insert_edge(n2_edge_ids[0], n2, n1_2)
        t1.insert_edge(n2_edge_ids[1], n2, n2_2)
        [t1.update_node_data(n, NodeData(t1.get_node_data(n).element)) for n in list(t1.get_nodes())]
        [t1.update_edge_data(e, EdgeData()) for e in list(t1.get_edges())]
        t1_per_idx.append(t1)
        t2 = _t.copy()
        t2.delete_edge(n1_edge_ids[0])
        t2.delete_edge(n1_edge_ids[1])
        t2.delete_edge(n2_edge_ids[0])
        t2.delete_edge(n2_edge_ids[1])
        t2.insert_edge(n1_edge_ids[0], n1, n1_1)
        t2.insert_edge(n1_edge_ids[1], n1, n2_2)
        t2.insert_edge(n2_edge_ids[0], n2, n1_2)
        t2.insert_edge(n2_edge_ids[1], n2, n2_1)
        [t2.update_node_data(n, NodeData(t2.get_node_data(n).element)) for n in list(t2.get_nodes())]
        [t2.update_edge_data(e, EdgeData()) for e in list(t2.get_edges())]
        t2_per_idx.append(t2)
    t1_per_idx = unrooted_parisomny(t1_per_idx)
    t2_per_idx = unrooted_parisomny(t2_per_idx)
    return t1_per_idx, t2_per_idx


def unrooted_parisomny(undir_g_per_idx: list[UndirectedGraph.Graph]) -> list[UndirectedGraph.Graph]:
    # To directed graph
    g_per_idx = []
    for g in undir_g_per_idx:
        _g = DirectedGraph.Graph()
        [_g.insert_node(n, g.get_node_data(n)) for n in g.get_nodes()]
        [_g.insert_edge(e, g.get_edge_ends(e)[0], g.get_edge_ends(e)[1], g.get_edge_data(e)) for e in g.get_edges()]
        g_per_idx.append(_g)

    # Break on any edge
    break_e_id = next(g_per_idx[0].get_edges())
    break_from, break_to, break_data = g_per_idx[0].get_edge(break_e_id)
    root_id = '_INTERNAL_ROOT'
    root_elem = '?'
    for i in range(seq_len):
        g_per_idx[i].insert_node(root_id, NodeData(root_elem))
        g_per_idx[i].insert_edge('ROOT_A', root_id, break_from, EdgeData())
        g_per_idx[i].insert_edge('ROOT_B', root_id, break_to, EdgeData())
        g_per_idx[i].delete_edge(break_e_id)
        # ensure all edges are pointing away from ROOT
        pending = [(None, root_id)]
        while pending:
            parent_n, n = pending.pop()
            for e in set(g_per_idx[i].get_inputs(n)):
                n_from, n_to, e_data = g_per_idx[i].get_edge(e)
                if n_from != parent_n:
                    # reverse edge
                    g_per_idx[i].delete_edge(e)
                    g_per_idx[i].insert_edge(e, n_to, n_from, e_data)
            for e in g_per_idx[i].get_outputs(n):
                n_to = g_per_idx[i].get_edge_to(e)
                pending.append((n, n_to))
    # print(f'{to_dot(g_per_idx[0])}')

    for i in range(seq_len):
        small_parsimony(g_per_idx[i])
        backtrack_to_create_elements_and_weights(g_per_idx[i])

    # Remove the root, making sure to sum the hamming dist of its edges when merging it back into a single edge
    for i in range(seq_len):
        new_hd = g_per_idx[i].get_edge_data('ROOT_A').hamming_distance + g_per_idx[i].get_edge_data(
            'ROOT_B').hamming_distance
        new_ed = EdgeData()
        new_ed.hamming_distance = new_hd
        g_per_idx[i].insert_edge(break_e_id, break_from, break_to, new_ed)
        g_per_idx[i].delete_edge('ROOT_A')
        g_per_idx[i].delete_edge('ROOT_B')
        g_per_idx[i].delete_node('_INTERNAL_ROOT')

    # To undirected graph
    _g_per_idx = []
    for g in g_per_idx:
        _g = UndirectedGraph.Graph()
        [_g.insert_node(n, g.get_node_data(n)) for n in g.get_nodes()]
        [_g.insert_edge(e, g.get_edge_from(e), g.get_edge_to(e), g.get_edge_data(e)) for e in g.get_edges()]
        _g_per_idx.append(_g)
    return _g_per_idx


def parismony_score(g_per_idx: list[UndirectedGraph.Graph]):
    min_parsimony_score = 0
    for e in g_per_idx[0].get_edges():
        for i in range(seq_len):
            min_parsimony_score += g_per_idx[i].get_edge_data(e).hamming_distance
    return min_parsimony_score


def output_tree(score: int, g_per_idx: list[UndirectedGraph.Graph]):
    print()
    print(f'{score}')
    for e in g_per_idx[0].get_edges():
        n_from, n_to, _ = g_per_idx[0].get_edge(e)
        seq_from = ''.join(g.get_node_data(n_from).element for g in g_per_idx)
        seq_to = ''.join(g.get_node_data(n_to).element for g in g_per_idx)
        dist = sum(g.get_edge_data(e).hamming_distance for g in g_per_idx)
        print(f'{seq_from}->{seq_to}:{int(dist)}')
        print(f'{seq_to}->{seq_from}:{int(dist)}')

seqs = {
    'DM1': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKEFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRIKIEELRQHLLKWGLTTPDKKHKKEPPFLW',
    'DM2': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKEFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRIKIEELRQHLLKWGLTTPDKKHQKEPPFLW',
    'DM3': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKNSTRWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKEFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRIKIEELRQHLLKWGFITPDEKHQKEPPFRW',
    'JT1/JT2': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKNSTRWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKEFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRIKTEELRQHLLKWGFFTPDEKHQKEPPFRW',
    'P1':  'PISPIETVPVKLKPGMDGPRVKQWPLTEEKIKALVEICTELEQXGKISKIGPENPYNTPVFAIKKKNSDKWRKLVDFRELNKRTQDFXEVQLGIPHPGGLKKKKSVTVLDVGDAYFSIPLDEDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYVDDLYVGSDLEIEQHRTKIXEFRQYLYKWGFYTPDRKYQKEPPFLW',
    'P2':  'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTELEKXGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSXPLDEXFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTXILEPFRXQNPDIVIYQYMDDLYVGSDLEIXQHRXKIEELRQHLWXWGFYTPDKKHQKEPPFLW',
    'P3':  'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKKTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRTKIEELRQHLLRWGFTTPDKKHQKEPPFLW',
    'P4':  'PISPIDTVPVKLKPGMDGPKVKQWPLTEEKIKALVEICAELEKXGKISKIGPENPYNTPVFAIKKKDXTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLXEDFRKYTAFTIPSTNNETPGIRYQYNVLPQGWKGSPAIFQCSMTKILEPFRKQNPDIVIYQYVDDLYVGSDLEIEQHRTKIEELRQHLWRWGFYTPDKKHQKEPPFLW',
    'P5':  'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIXPENPYNTPVFAIKKKDSTKWRKLVDFRELNKRTQDFXEVQLXIPHPAGLKKKKSVTVLDVGDAYFSVPLDEDFRKYTAFTIPSTNNETPGVRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQHPDXVIYQYMDDLYVGSDLEIEQHRTKIEELRQHLLRWGFTTPDKKHQKXPPFLW',
    'P6':  'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDXDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKHNPEIVIYQYVDDLYVGSDLEIGQHRTKIEELRQHLLRWGFXTPDKKHQKEPPFLW',
    'P7':  'PISPIETVPVKLKPGMDGPRVKQWPLTEEKIKALVEICXELEKEGKISKIGPENPYNTPVFAIKKKDSTXWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKXSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIIIYQYMDDLYVGSDLDIGQHRTKXEELRQHLLRWGFYTPDKKHQKEPPFLW',
    'P8':  'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKXSTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRTKIEELRQHLLKWGFTTPDKKHQKEPPFLW',
    'P9':  'PISPIETVPVKLKPGMDGPRVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDEDFRKYTAFTIPSVNNETPGIRYQYNVLPQGWKGSPAIFQCSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRTKIEELRQHLLKWGFXTPDKKHQKEPPFLW',
    'P10': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPIFAIKKKDSTKWRKLVDFRELNKKTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRTKIEELRQHLLKWGFTTPDKKHQKEPPFLW',
    'P11': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIRALVEICTELEKEGKISKIGPENPYNTPVFAIKKKNSNRWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSVNNETPGIRYQYNVLPQGWKGSPALFQSSMTKILEPFRKQNPDIVIYQYVDDLYVGSDLEIGQHRTKTEELRQHLLRWGFFTPDEKHQKEPPFRW',
    'P12': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSTNNETPGIRYQYNVLPQGWKGSPAIFQSSMTRILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRTKIEELRQHLLRWGXTTPDXKHQKEPPFLW',
    'P13': 'PISPIXTVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPIFAIKKKDSSKWRKLVDFRELNKKTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPDIVIYQYMDDLYVGSDLEIGQHRTKIEELRQHLLKWGFTTPDKKHQKEPPFLW',
    'P14': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICAELEQXGKISKIGPENPYNTPVFAIKKKDSTKWRKLXDFRELNKRTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSXPLXEDFRKYTAFTIPSXNNATPGIRYQYNVLPQGWKGSPAIFQSSMTKILEPFRKQNPXXXIYQYXDDLYVGSDLEIXQHRTKIXXLREHLWKWGFYTPDKKHQKEPPFLW',
    'P15': 'PISPIETVPVKLKPGMDGPKVKQWPLTEEKIKALVEICTEMEKEGKISKIGPENPYNTPVFAIKKKDSTKWRKLVDFRELNKKTQDFWEVQLGIPHPAGLKKKKSVTVLDVGDAYFSVPLDKDFRKYTAFTIPSINNETPGIRYQYNVLPQGWKGSPAIFQSSMIKILEPFRKQNPDIVIYQYMDDLYVGSDLEIEXHRXKIEELRQHLLRWGFTTPDKKHQKEPPFLW',
}
seq_len = len(next(iter(seqs.values())))

hamming = {}
for s1, s2 in product(seqs.values(), repeat=2):
    mismatch = 0
    for ch1, ch2 in zip(s1, s2):
        if ch1 != ch2:
            mismatch += 1
    hamming[s1, s2] = mismatch

dm = DistanceMatrix(hamming)

_next_edge_id = 0
def gen_edge_id():
    global _next_edge_id
    _next_edge_id += 1
    return f'_E{_next_edge_id}'
_next_node_id = 0
def gen_node_id():
    global _next_node_id
    _next_node_id += 1
    return f'_INTERNAL{_next_node_id}'
t = neighbour_joining_phylogeny(dm, gen_node_id, gen_edge_id)

t_per_idx = []
for i in range(seq_len):
    _t: UndirectedGraph.Graph[str, NodeData, str, EdgeData] = t.copy()
    for n in list(_t.get_nodes()):
        if n.startswith('_INTERNAL'):
            _t.update_node_data(n, NodeData('?'))
        else:
            _t.update_node_data(n, NodeData(n[i]))
    for e in list(_t.get_edges()):
        _t.update_edge_data(e, EdgeData())
    t_per_idx.append(_t)

score = math.inf
new_tree = unrooted_parisomny(t_per_idx)
new_score = parismony_score(new_tree)
while new_score < score:
    # output_tree(new_score, new_tree)
    print(f'{new_score}')
    print(f'{to_dot(new_tree, seqs)}')
    tree = new_tree
    score = new_score
    internal_nodes = {n for n in tree[0].get_nodes() if tree[0].get_degree(n) > 1}
    internal_edges = {e for e in tree[0].get_edges() if len(internal_nodes.intersection(set(tree[0].get_edge_ends(e)))) == 2}
    for internal_edge in internal_edges:
        for nn_tree in nn_swap(internal_edge, tree):
            nn_score = parismony_score(nn_tree)
            if nn_score < new_score:
                new_tree = nn_tree
                new_score = nn_score