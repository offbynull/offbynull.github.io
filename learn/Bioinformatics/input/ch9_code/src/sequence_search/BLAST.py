from collections import defaultdict
from itertools import product
from sys import stdin
from typing import Callable, Generator, Any

import yaml

from helpers.Utils import slide_window
from sequence_search.SearchUtils import hamming_distance














# This is global alignment copied over from the alignment chapter.
# This is global alignment copied over from the alignment chapter.
# This is global alignment copied over from the alignment chapter.
# This is global alignment copied over from the alignment chapter.
# This is global alignment copied over from the alignment chapter.
# This is global alignment copied over from the alignment chapter.
def backtrack(
        node_matrix: list[list[Any]]
) -> tuple[float, list[tuple[str, str]]]:
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
        v: list[str],
        w: list[str],
        weight_lookup_func: Callable[[str | None, str | None], float]
) -> tuple[float, list[tuple[str, str]]]:
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
                node_matrix[v_node_idx - 1][w_node_idx - 1][0] + weight_lookup_func(v_elem, w_elem),
                (v_elem, w_elem),
                '↘'
            ])
        if v_node_idx > 0:
            v_elem = v[v_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx - 1][w_node_idx][0] + weight_lookup_func(v_elem, None),
                (v_elem, None),
                '↓'
            ])
        if w_node_idx > 0:
            w_elem = w[w_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx][w_node_idx - 1][0] + weight_lookup_func(None, w_elem),
                (None, w_elem),
                '→'
            ])
        if parents:  # parents wil be empty if v_node_idx and w_node_idx were both 0
            node_matrix[v_node_idx][w_node_idx] = max(parents, key=lambda x: x[0])
    return backtrack(node_matrix)


class ScoringMatrix:
    def __init__(self, score_map: dict[tuple[str, str], float], indel_score: float):
        self.score_map = score_map
        self.indel_score = indel_score

    def compute_score(self, ch1: str | None, ch2: str | None) -> float:
        return self.indel_score if ch1 is None or ch2 is None else self.score_map[ch1, ch2]

    @staticmethod
    def parse(matrix: str):
        score_map = {}
        matrix = matrix.strip()
        lines = matrix.split('\n')
        header_alphabet = lines[0].split()
        indel_ch = header_alphabet[-1]
        for line in lines[1:]:
            line_split = line.split()
            elem_row = line_split[0]
            for val, elem_col in zip(line_split[1:], header_alphabet):
                if elem_col == indel_ch or elem_row == indel_ch:
                    continue
                score_map[elem_row, elem_col] = float(val)
        indel_score = float(lines[1].split()[-1])
        return ScoringMatrix(score_map, indel_score)

    @staticmethod
    def parse_alphabet(matrix: str):
        matrix = matrix.strip()
        lines = matrix.split('\n')
        header_alphabet = lines[0].split()
        return ''.join(header_alphabet[:-1])  # strip indel char off













# MARKDOWN_BUILD
def find_similar_kmers(
        kmer: str,
        alphabet: str,
        score_function: Callable[[str, str], float],
        score_min: float
) -> Generator[str, None, None]:
    k = len(kmer)
    for neighbouring_kmer in product(alphabet, repeat=k):
        neighbouring_kmer = ''.join(neighbouring_kmer)
        alignment_score = score_function(kmer, neighbouring_kmer)
        if alignment_score >= score_min:
            yield neighbouring_kmer


def create_database(
        seqs: set[str],
        k: int,
        alphabet: str,
        alignment_score_function: Callable[[str, str], float],
        alignment_min: float
) -> dict[str, set[tuple[str, int]]]:
    db = defaultdict(set)
    for seq in seqs:
        for kmer, idx in slide_window(seq, k):
            for neighbouring_kmer in find_similar_kmers(kmer, alphabet, alignment_score_function, alignment_min):
                db[neighbouring_kmer].add((seq, idx))
    return db
# MARKDOWN_BUILD


# MARKDOWN_FIND
def find_hsps(
        seq: str,
        k: int,
        db: dict[str, set[tuple[str, int]]],
        score_function: Callable[[str, str], float],
        score_min: float
):
    # Find high scoring segment pairs
    hsp_records = set()
    for kmer1, idx1_begin in slide_window(seq, k):
        # Find sequences for this kmer in the database
        found_seqs = db.get(kmer1, None)
        if found_seqs is None:
            continue
        # For each match, extend left-and-right until the alignment score begins to decrease
        for seq2, idx2_begin in found_seqs:
            last_idx1_begin, last_idx1_end = idx1_begin, idx1_begin + k
            last_idx2_begin, last_idx2_end = idx2_begin, idx2_begin + k
            last_kmer1 = seq[last_idx1_begin:last_idx1_end]
            last_kmer2 = seq2[last_idx2_begin:last_idx2_end]
            last_score = score_function(last_kmer1, last_kmer2)
            last_k = k
            while True:
                new_idx1_begin, new_idx1_end = last_idx1_begin, last_idx1_end
                new_idx2_begin, new_idx2_end = last_idx2_begin, last_idx2_end
                if new_idx1_begin > 0 and new_idx2_begin > 0:
                    new_idx1_begin -= 1
                    new_idx2_begin -= 1
                if new_idx1_begin < len(seq) - 1 and new_idx2_end < len(seq2) - 1:
                    new_idx1_end = new_idx1_end + 1
                    new_idx2_end = new_idx2_end + 1
                new_kmer1 = seq[new_idx1_begin:new_idx1_end]
                new_kmer2 = seq2[new_idx2_begin:new_idx2_end]
                new_score = score_function(new_kmer1, new_kmer2)
                # If current extension decreased the alignment score, stop. Add the PREVIOUS extension as a high-scoring
                # segment pair only if it scores high enough to be considered
                if new_score < last_score:
                    if last_score >= score_min:
                        record = last_score, last_k, (last_idx1_begin, seq), (last_idx2_begin, seq2)
                        hsp_records.add(record)
                    break
                last_score = new_score
                last_k = new_idx1_end - new_idx1_begin
                last_idx1_begin, last_idx1_end = new_idx1_begin, new_idx1_end
                last_idx2_begin, last_idx2_end = new_idx2_begin, new_idx2_end
                last_kmer1 = new_kmer1
                last_kmer2 = new_kmer2
    return hsp_records
# MARKDOWN_FIND


# https://en.wikipedia.org/wiki/BLAST_(biotechnology)#Algorithm


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        db_seqs = data['database_sequences']
        query_seq = data['query_sequence']
        k = data['k']
        min_neighbourhood_score = data['min_neighbourhood_score']
        min_extension_score = data['min_extension_score']
        scoring_matrix = data['scoring_matrix']
        print(f'Running BLAST using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        db_seqs_reversed = defaultdict(set)
        db_seqs_reversed.update(((v, k) for k, v in db_seqs.items()))
        alphabet = ScoringMatrix.parse_alphabet(scoring_matrix)
        scoring_matrix = ScoringMatrix.parse(scoring_matrix)
        scoring_func = lambda s1, s2: global_alignment(s1, s2, scoring_matrix.compute_score)[0]
        db = create_database(set(db_seqs.values()), k, alphabet, scoring_func, min_neighbourhood_score)
        print()
        print(f'Database contains {len(db)} {k}-mers')
        print()
        print(f'Scanning the database for {k}-mers in {query_seq}...')
        print()
        hsp_set = find_hsps(query_seq, k, db, scoring_func, min_extension_score)
        for score, k, (query_seq_idx, query_seq), (db_seq_idx, db_seq) in hsp_set:
            print(f' * {k=} / {score=}')
            print(f'   ')
            print(f'   ```')
            print(f'   Query k-mer: {query_seq[query_seq_idx:query_seq_idx + k]} @ {query_seq_idx}')
            print(f'   DB k-mer:    {db_seq[db_seq_idx:db_seq_idx + k]} @ {db_seq_idx} {[v for k, v in db_seqs_reversed.items() if k == db_seq]}')
            print(f'   ```')
            print(f'   ')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()