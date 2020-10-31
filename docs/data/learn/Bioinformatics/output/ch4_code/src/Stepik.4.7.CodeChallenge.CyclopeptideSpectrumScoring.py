import typing
from collections import Counter
from itertools import permutations, accumulate
from typing import Tuple, List

with open('/home/user/Downloads/dataset_240282_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
cyclopeptide = data[0].strip()
expected_spectrum = Counter([int(m) for m in data[1].strip().split()])


mass_table = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 'D': 115,
              'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186}


def cyclopeptide_spectrum(peptide: str) -> typing.Counter[int]:
    prefix_masses = [0]
    for i, ch in enumerate(peptide):
        w = mass_table[ch]
        prev_mass = prefix_masses[i]
        next_mass = prev_mass + w
        prefix_masses.append(next_mass)
    ret = [0]
    for k_end in range(0, len(prefix_masses)):
        for k_start in range(0, k_end):
            min_mass = prefix_masses[k_start]
            max_mass = prefix_masses[k_end]
            ret.append(max_mass - min_mass)
            if k_start > 0 and k_end < len(peptide):
                ret.append(prefix_masses[-1] - (prefix_masses[k_end] - prefix_masses[k_start]))
    return Counter(ret)


cp_spectrum = cyclopeptide_spectrum(cyclopeptide)

# print(f'{cp_spectrum}')
# print(f'{expected_spectrum}')
score = sum([min(cp_spectrum[k], expected_spectrum[k]) for k in cp_spectrum.keys() | expected_spectrum.keys()])
print(f'{score}')