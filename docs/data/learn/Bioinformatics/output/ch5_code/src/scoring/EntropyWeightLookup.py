from collections import Counter
from math import log
from typing import Tuple, Optional

from scoring.WeightLookup import WeightLookup, ELEM


# MARKDOWN
class EntropyWeightLookup(WeightLookup):
    def __init__(self, indel_weight: float):
        self.indel_weight = indel_weight

    @staticmethod
    def _calculate_entropy(values: Tuple[float, ...]) -> float:
        ret = 0.0
        for value in values:
            ret += value * (log(value, 2.0) if value > 0.0 else 0.0)
        ret = -ret
        return ret

    def lookup(self, *elements: Tuple[Optional[ELEM], ...]):
        if None in elements:
            return self.indel_weight

        counts = Counter(elements)
        total = len(elements)
        probs = tuple(v / total for k, v in counts.most_common())
        entropy = EntropyWeightLookup._calculate_entropy(probs)

        return -entropy
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dims = int(input())
        seq_elems = [input() for _ in range(dims)]
        seq_elems = [None if e == '' else e for e in seq_elems]
        indel_weight = float(input())
        weight_lookup = EntropyWeightLookup(indel_weight)
        print(f'Given the elements {[e for e in seq_elems]}, the entropy score for these elements is {weight_lookup.lookup(*seq_elems)} (INDEL={indel_weight}).', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()