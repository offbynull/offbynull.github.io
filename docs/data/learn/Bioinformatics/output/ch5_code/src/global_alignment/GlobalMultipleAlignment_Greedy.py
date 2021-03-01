from collections import Counter
from itertools import combinations
from typing import List, TypeVar, Tuple, Optional, Union

from global_alignment import GlobalAlignment_Matrix
from scoring.WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')
ELEM_OR_COLUMN = Union[
    Optional[ELEM],
    List[ELEM]
]


# MARKDOWN
class ProfileWeightLookup(WeightLookup):
    def __init__(self, total_seqs: int, backing_2d_lookup: WeightLookup):
        self.total_seqs = total_seqs
        self.backing_wl = backing_2d_lookup

    def lookup(self, *elements: Tuple[ELEM_OR_COLUMN, ...]):
        col: Tuple[ELEM, ...] = elements[0]
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


def global_alignment(
        seqs: List[List[ELEM]],
        weight_lookup_2way: WeightLookup,
        weight_lookup_multi: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ...]]]:
    seqs = seqs[:]  # copy
    # Get initial best 2-way alignment
    highest_res = None
    highest_seqs = None
    for s1, s2 in combinations(seqs, r=2):
        if s1 is s2:
            continue
        res = GlobalAlignment_Matrix.global_alignment(s1, s2, weight_lookup_2way)
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
                [GlobalAlignment_Matrix.global_alignment(s1, s2, profile_weight_lookup) for s2 in seqs],
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
    # Recalculate score based on multi weight lookup
    final_weight = sum(weight_lookup_multi.lookup(*elems) for elems in final_alignment)
    return final_weight, final_alignment
# MARKDOWN


# x = global_alignment(
#     [list('TRELLO'), list('MELLOW'), list('HELLO'), list('CELLOS')],
#     ConstantWeightLookup(1, -1, -1)
# )
# print(f'{x}')


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dims = int(input())
        seqs = [list(input()) for _ in range(dims)]
        matrix_type = input()
        if matrix_type == 'embedded_score_matrix':
            indel_weight = float(input())
            weights_data = ''
            try:
                while True:
                    weights_data += input() + '\n'
            except EOFError:
                ...
        elif matrix_type == 'file_score_matrix':
            indel_weight = float(input())
            path = input()
            with open(path, mode='r', encoding='utf-8') as f:
                weights_data = f.read()
        else:
            raise ValueError('Bad score matrix type')
        weights_data = weights_data.strip()
        parsed_weights_data = dict()
        for line in weights_data.split('\n'):
            line_split = line.split()
            elems = tuple(line_split[:-1])
            weight = float(line_split[-1])
            parsed_weights_data[elems] = weight
        weight_lookup = Table2DWeightLookup(parsed_weights_data, indel_weight)
        weight, elems = global_alignment(seqs, weight_lookup)
        print(f'Given the sequences {["".join(s) for s in seqs]} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the global alignment is...', end="\n\n")
        print(f'````', end='\n')
        for i in range(dims):
            print(f'{"".join("-" if e[i] is None else e[i] for e in elems)}')
        print(f'````', end='\n\n')
        print(f'Weight: {weight}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
