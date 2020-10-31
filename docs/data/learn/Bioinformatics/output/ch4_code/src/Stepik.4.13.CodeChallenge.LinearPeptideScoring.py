import typing
from collections import Counter
from itertools import permutations, accumulate
from typing import Tuple, List

with open('/home/user/Downloads/dataset_240288_1.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
peptide = data[0].strip()
expected_spectrum = Counter([int(m) for m in data[1].strip().split()])


mass_table = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 'D': 115,
              'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186}


def linear_peptid_spectrum(peptide: str) -> typing.Counter[int]:
    ret = Counter([0])
    for i in range(len(peptide)):
        ret += Counter(list(accumulate([mass_table[ch] for ch in peptide[i:]])))
    return ret


lp_spectrum = linear_peptid_spectrum(peptide)

# print(f'{cp_spectrum}')
# print(f'{expected_spectrum}')
score = sum([min(lp_spectrum[k], expected_spectrum[k]) for k in lp_spectrum.keys() | expected_spectrum.keys()])
print(f'{score}')