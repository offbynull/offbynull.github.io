from itertools import combinations
from typing import Tuple, Optional

from scoring.WeightLookup import WeightLookup, ELEM, Table2DWeightLookup


# MARKDOWN
class SumOfPairsWeightLookup(WeightLookup):
    def __init__(self, backing_2d_lookup: WeightLookup):
        self.backing_wl = backing_2d_lookup

    def lookup(self, *elements: Tuple[Optional[ELEM], ...]):
        return sum(self.backing_wl.lookup(a, b) for a, b in combinations(elements, r=2))
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dims = int(input())
        seq_elems = [input() for _ in range(dims)]
        seq_elems = [None if e == '' else e for e in seq_elems]
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
        backing_weight_lookup = Table2DWeightLookup.create_from_2d_matrix_str(weights_data, indel_weight)
        weight_lookup = SumOfPairsWeightLookup(backing_weight_lookup)
        print(f'Given the elements {[e for e in seq_elems]} and the backing score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the sum-of-pairs score for these elements is {weight_lookup.lookup(*seq_elems)}.', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
    # print(f"{list(combinations(['I', None, 'I', 'V'], r=2))}")