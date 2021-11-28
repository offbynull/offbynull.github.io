import json
import lzma
import math
import multiprocessing
import re
from abc import ABC, abstractmethod
from collections import Counter
from itertools import product, combinations
from random import sample
from statistics import mean
from sys import stdin
from typing import Optional, TypeVar, Union, Any

from distance_matrix.DistanceMatrix import DistanceMatrix
from graph.UndirectedGraph import Graph
from phylogeny.NeighbourJoiningPhylogeny import neighbour_joining_phylogeny, to_dot


## THIS IS ALL LIFTED FROM THE SEQUENCE ALIGNMENT CHAPTER
## THIS IS ALL LIFTED FROM THE SEQUENCE ALIGNMENT CHAPTER
## THIS IS ALL LIFTED FROM THE SEQUENCE ALIGNMENT CHAPTER
## THIS IS ALL LIFTED FROM THE SEQUENCE ALIGNMENT CHAPTER
## THIS IS ALL LIFTED FROM THE SEQUENCE ALIGNMENT CHAPTER
## THIS IS ALL LIFTED FROM THE SEQUENCE ALIGNMENT CHAPTER
from sequence_phylogeny import SmallParsimony

ELEM = TypeVar('ELEM')
ELEM_OR_COLUMN = Union[
    Optional[ELEM],
    list[ELEM]
]


class WeightLookup(ABC):
    @abstractmethod
    def lookup(self, *elements: tuple[Optional[ELEM], ...]):
        ...


class TableWeightLookup(WeightLookup):
    def __init__(self, weight_lookup: dict[tuple[ELEM, ...], float], indel_weight: float):
        self.weight_lookup = weight_lookup
        self.indel_weight = indel_weight

    @staticmethod
    def create_from_2d_matrix_file(weight_lookup_path: str, indel_weight: float):
        with open(weight_lookup_path, mode='r', encoding='utf-8') as f:
            data = f.read()
        return TableWeightLookup.create_from_2d_matrix_str(data, indel_weight)

    @staticmethod
    def create_from_2d_matrix_str(data: str, indel_weight: float):
        weight_lookup = {}
        lines = data.strip().split('\n')
        aa_row = lines[0].strip().split()
        for line in lines[1:]:
            vals = line.strip().split()
            aa2 = vals[0]
            weight = vals[1:]
            for aa1, weight in zip(aa_row, weight):
                weight_lookup[(aa1, aa2)] = float(weight)
        return TableWeightLookup(weight_lookup, indel_weight)

    def lookup(self, *elements: tuple[Optional[ELEM], ...]):
        if None in elements:
            return self.indel_weight
        return self.weight_lookup[elements]


def backtrack(
        node_matrix: list[list[Any]]
) -> tuple[float, list[tuple[ELEM, ELEM]]]:
    v_node_idx = len(node_matrix) - 1
    w_node_idx = len(node_matrix[0]) - 1
    final_weight = node_matrix[v_node_idx][w_node_idx][0]
    alignment = []
    while v_node_idx != 0 or w_node_idx != 0:
        _, elems, backtrack_ptr = node_matrix[v_node_idx][w_node_idx]
        if backtrack_ptr == '↓':
            v_node_idx -= 1
        elif backtrack_ptr == '→':
            w_node_idx -= 1
        elif backtrack_ptr == '↘':
            v_node_idx -= 1
            w_node_idx -= 1
        alignment.append(elems)
    return final_weight, alignment[::-1]


def global_alignment(
        v: list[ELEM],
        w: list[ELEM],
        weight_lookup: WeightLookup
) -> tuple[float, list[tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    node_matrix = []
    for v_node_idx in range(v_node_count):
        row = []
        for w_node_idx in range(w_node_count):
            row.append([-1.0, (None, None), '?'])
        node_matrix.append(row)
    node_matrix[0][0][0] = 0.0           # source node weight
    node_matrix[0][0][1] = (None, None)  # source node elements (elements don't matter for source node)
    node_matrix[0][0][2] = '↘'           # source node backtracking edge (direction doesn't matter for source node)
    for v_node_idx, w_node_idx in product(range(v_node_count), range(w_node_count)):
        parents = []
        if v_node_idx > 0 and w_node_idx > 0:
            v_elem = v[v_node_idx - 1]
            w_elem = w[w_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx - 1][w_node_idx - 1][0] + weight_lookup.lookup(v_elem, w_elem),
                (v_elem, w_elem),
                '↘'
            ])
        if v_node_idx > 0:
            v_elem = v[v_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx - 1][w_node_idx][0] + weight_lookup.lookup(v_elem, None),
                (v_elem, None),
                '↓'
            ])
        if w_node_idx > 0:
            w_elem = w[w_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx][w_node_idx - 1][0] + weight_lookup.lookup(None, w_elem),
                (None, w_elem),
                '→'
            ])
        if parents:  # parents wil be empty if v_node_idx and w_node_idx were both 0
            node_matrix[v_node_idx][w_node_idx] = max(parents, key=lambda x: x[0])
    return backtrack(node_matrix)


class ProfileWeightLookup(WeightLookup):
    def __init__(self, total_seqs: int, backing_2d_lookup: WeightLookup):
        self.total_seqs = total_seqs
        self.backing_wl = backing_2d_lookup

    def lookup(self, *elements: tuple[ELEM_OR_COLUMN, ...]):
        col: tuple[ELEM, ...] = elements[0]
        elem: ELEM = elements[1]

        if col is None:
            return self.backing_wl.lookup(elem, None)  # should map to indel score
        elif elem is None:
            return self.backing_wl.lookup(None, col[0])  # should map to indel score
        else:
            probs = {elem: count / self.total_seqs for elem, count in Counter(e for e in col if e is not None).items()}
            ret = 0.0
            for p_elem, prob in probs.items():
                val = self.backing_wl.lookup(elem, p_elem) * prob
                ret = max(val, ret)
            return ret


def greedy_multiple_alignment(
        seqs: list[list[ELEM]],
        weight_lookup_2way: WeightLookup
) -> list[tuple[ELEM, ...]]:
    seqs = seqs[:]  # copy
    # Get initial best 2-way alignment
    highest_res = None
    highest_seqs = None
    for s1, s2 in combinations(seqs, r=2):
        if s1 is s2:
            continue
        res = global_alignment(s1, s2, weight_lookup_2way)
        if highest_res is None or res[0] > highest_res[0]:
            highest_res = res
            highest_seqs = s1, s2
    seqs.remove(highest_seqs[0])
    seqs.remove(highest_seqs[1])
    total_seqs = 2
    final_alignment = highest_res[1]
    # Build out profile matrix from alignment and continually add to it using 2-way alignment
    if seqs:
        s1 = highest_res[1]
        while seqs:
            profile_weight_lookup = ProfileWeightLookup(total_seqs, weight_lookup_2way)
            _, alignment = max(
                [global_alignment(s1, s2, profile_weight_lookup) for s2 in seqs],
                key=lambda x: x[0]
            )
            # pull out s1 from alignment and flatten for next cycle
            s1 = []
            for e in alignment:
                if e[0] is None:
                    s1 += [((None, ) * total_seqs) + (e[1], )]
                else:
                    s1 += [(*e[0], e[1])]
            # pull out s2 from alignment and remove from seqs
            s2 = [e for _, e in alignment if e is not None]
            seqs.remove(s2)
            # increase seq count
            total_seqs += 1
        final_alignment = s1
    return final_alignment



def to_weight_table(lines: list[str]) -> dict[tuple[Optional[str], Optional[str]], float]:
    ret = {}
    header = lines[0].split()
    for data in lines[1:]:
        elems = data.split()
        e1 = elems[0]
        for e2, weight in zip(header, elems[1:]):
            ret[e1, e2] = float(weight)
    return ret


def to_dot(g: Graph[str, dict[str, str], str, float], scale=0.1) -> str:
    ret = 'graph G {\n'
    ret += ' layout=neato\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=box, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    n_lookup = {n: (re.sub(r"\W+", '', n), n.replace('\n', '\\n')) for n in nodes}
    for n in nodes:
        n_id, n_label = n_lookup[n]
        n_seq = g.get_node_data(n)['seq']
        n_seq_split = '\\n'.join(n_seq[i:i+100] for i in range(0, len(n_seq), 100))
        ret += f'{n_id} [label="{n_label}\\n\\n seq\\n{n_seq_split}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        n1_id, _ = n_lookup[n1]
        n2_id, _ = n_lookup[n2]
        ret += f'{n1_id} -- {n2_id} [label="{weight:.2f}", len={weight*scale}]\n'
    ret += '}'
    return ret


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        # Read matrix
        lines = stdin.readlines()
        jsonpath = lines.pop(0).strip()
        sample_size = int(lines.pop(0).strip())
        edge_len_scale = float(lines.pop(0).strip())
        weight_indel = float(lines.pop(0))
        weight_lines = [l.rstrip() for l in lines]
        weight_lookup = TableWeightLookup(to_weight_table(weight_lines), weight_indel)
        with lzma.open(jsonpath, mode='rt', encoding='utf-8') as f:
            seqs = json.loads(f.read())
        seq_ids_sample = sample(list(seqs), sample_size)
        elem_types = ''.join({ch for s_id in seq_ids_sample for seq in seqs[s_id] for ch in seq})
        print(f'Given a random sample of {sample_size} sequences from {jsonpath} and the following alignment weights...')
        print()
        print('```')
        for l in weight_lines:
            print(l)
        print('```')
        print()
        print(f'INDEL={weight_indel}')
        print()
        print(f'The tree generated by neighbour joining phylogeny ALONG WITH INFERRED ANCESTRAL SEQUENCES is (distances measured using global alignment, edge lengths scaled to {edge_len_scale}) ...')
        print()
        relatedness = {}
        with multiprocessing.Pool(4) as p:
            for s1 in seq_ids_sample:
                tests = [(s1, s2) for s2 in seq_ids_sample if (s1, s2) not in relatedness]
                jobs = [(list(seqs[s1]), list(seqs[s2]), weight_lookup) for s1, s2 in tests]
                align_results = p.starmap(global_alignment, jobs)
                for (test_s1, test_s2), (weight, _) in zip(tests, align_results):
                    relatedness[test_s1, test_s2] = weight
                    relatedness[test_s2, test_s1] = weight
        # convert final alignment weights to distances -- There are some assumptions being made here, specifically that
        # that for sequences X and Y, max(alignment_score(X,X), alignment_score(Y,Y)) is the best possible alignment
        # score you can have. Depending on the weight matrix for alignment, this may not be true, but it's probably an
        # okay assumption to max.
        #
        #   best_possible_alignment_score = max(alignment_score(X,X), alignment_score(Y,Y))
        #
        # The distance is measured by subtracting alignment_score(X,Y) from this best alignment score
        #
        #  distance = best_possible_alignment_score - alignment_score(X,Y)
        distances = {}
        for s1, s2 in product(seq_ids_sample, repeat=2):
            if s1 == s2:
                distances[s1, s2] = 0
                continue
            peak = max(relatedness[s1, s1], relatedness[s2, s2])
            distances[s1, s2] = peak - relatedness[s1, s2]
        dist_mat = DistanceMatrix(distances)
        _next_edge_id = 0
        def gen_edge_id():
            nonlocal _next_edge_id
            _next_edge_id += 1
            return f'E{_next_edge_id}'
        _next_node_id = 0
        def gen_node_id():
            nonlocal _next_node_id
            _next_node_id += 1
            return f'N{_next_node_id}'
        tree = neighbour_joining_phylogeny(dist_mat, gen_node_id, gen_edge_id)
        #
        # Do the multiple alignment
        #
        multiple_align_res = greedy_multiple_alignment(
            [list(seqs[s]) for s in seq_ids_sample],
            weight_lookup
        )
        multiple_align_len = len(multiple_align_res)
        # Inject seqs into tree
        [tree.update_node_data(n, {}) for n in tree.get_nodes()]
        for idx, seq_name in enumerate(seq_ids_sample):
            n_data = tree.get_node_data(seq_name)
            aligned_seq = ''.join(('-' if column[idx] is None else column[idx]) for column in multiple_align_res)
            n_data['seq'] = aligned_seq
        # Perform small parsimony
        root = next(n for n in tree.get_nodes() if tree.get_degree(n) > 1)  # just pick any non-leaf node to be the root
        SmallParsimony.populate_distance_sets(
            tree,
            root,
            multiple_align_len,
            lambda n: tree.get_node_data(n)['seq'],
            lambda n, seq: tree.get_node_data(n).update({'seq': seq}),
            lambda n, idx: tree.get_node_data(n).get(f'dist_set_{idx}', {}),
            lambda n, idx, ds: tree.get_node_data(n).update({f'dist_set_{idx}': ds}),
            lambda e1, e2: -weight_lookup.lookup(e1 if e1 != '-' else None, e2 if e2 != '-' else None),
            elem_types
        )
        print()
        print('```{dot}')
        print(f'{to_dot(tree, scale=edge_len_scale)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()