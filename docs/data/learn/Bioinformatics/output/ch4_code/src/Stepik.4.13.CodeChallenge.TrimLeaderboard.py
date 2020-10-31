import typing
from collections import Counter
from itertools import permutations, accumulate
from typing import Tuple, List, Set

with open('/home/user/Downloads/dataset_240288_3(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
leaderboard = data[0].strip().split()
expected_spectrum = Counter([int(m) for m in data[1].strip().split()])
n = int(data[2].strip())


mass_table = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 'D': 115,
              'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186}


class HashableList(list):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)
        self._cached_hash = None

    def __hash__(self):
        if self._cached_hash is None:
            self._cached_hash = hash(tuple(self))
        return self._cached_hash


def linear_peptid_spectrum(peptide: str) -> typing.Counter[int]:
    ret = Counter([0])
    for i in range(len(peptide)):
        ret += Counter(list(accumulate([mass_table[ch] for ch in peptide[i:]])))
    return ret


def linear_score(peptide_spectrum: typing.Counter[int], expected_spectrum: typing.Counter[int]) -> int:
    keys = peptide_spectrum.keys() | expected_spectrum.keys()
    return sum([min(peptide_spectrum[k], expected_spectrum[k]) for k in keys])


def trim_leaderboard(leaderboard: List[str], expected_spectrum: typing.Counter[int], n: int) -> List[str]:
    if len(leaderboard) == 0:
        return leaderboard
    scores = [linear_score(linear_peptid_spectrum(p), expected_spectrum) for p in leaderboard]
    sorted_peptides_and_scores = list(sorted(zip(leaderboard, scores), key=lambda x: x[1], reverse=True))
    for j in range(n + 1, len(sorted_peptides_and_scores)):
        if sorted_peptides_and_scores[n][1] > sorted_peptides_and_scores[j][1]:
            return [p for p, _ in sorted_peptides_and_scores[:j-1]]
    return [p for p, _ in sorted_peptides_and_scores]


leaderboard = trim_leaderboard(leaderboard, expected_spectrum, n)

# print(f'{cp_spectrum}')
# print(f'{expected_spectrum}')
print(f'{" ".join(leaderboard)}')