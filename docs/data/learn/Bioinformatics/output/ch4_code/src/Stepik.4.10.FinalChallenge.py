
from collections import Counter
from random import Random
from typing import List

from NoisyLeaderboardCyclopeptideSequencing import sequence_cyclic_peptide
from NoisyGroupPeptides import group_peptides_within_tolerance
from NoisyScoreSpectrums import score_spectrums
from NoisySpectrumConvolution import spectrum_convolution
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from Utils import get_unique_amino_acid_masses_as_dict, HashableList, rotate, N

# with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
#     data = f.read()
# cyclic_peptide_experimental_spectrum = [float(w) for w in data.strip().split()]
# cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case


r = Random(1)
fake_peptide = [147, 97, 147, 147, 114, 128, 163, 99, 71, 156]
cyclopeptide_exp_spec = theoretical_spectrum_of_cyclic_peptide(fake_peptide, mass_table=get_unique_amino_acid_masses_as_dict())
cyclopeptide_exp_spec = [float(w) for w in cyclopeptide_exp_spec]
# remove 0.2x randomly (but re-add the final mass if it was removed)
fake_peptide_mass = cyclopeptide_exp_spec[-1]
r.shuffle(cyclopeptide_exp_spec)
cyclopeptide_exp_spec = cyclopeptide_exp_spec[:int(len(cyclopeptide_exp_spec) * 0.8)]
cyclopeptide_exp_spec.sort()
if cyclopeptide_exp_spec[-1] != fake_peptide_mass:
    cyclopeptide_exp_spec += [fake_peptide_mass]
# add noise
cyclopeptide_exp_spec = [w + r.uniform(-0.3, 0.3) for w in cyclopeptide_exp_spec]
# add weight of +1 charge (a single proton)
cyclopeptide_exp_spec = [w + 1.007 for w in cyclopeptide_exp_spec]
# add 2.0x junk masses
for i in range(0, len(cyclopeptide_exp_spec) * 2):
    idx = r.randrange(0, len(cyclopeptide_exp_spec))
    junk_val = cyclopeptide_exp_spec[idx] + r.uniform(0, 50)
    cyclopeptide_exp_spec.append(junk_val)
# sort
cyclopeptide_exp_spec.sort()


m = 150
n = 1000

cyclopeptide_exp_spec = [round(m - 1.007, 1) for m in cyclopeptide_exp_spec]  # remove mass for +1 charge and round

amino_acid_masses = spectrum_convolution(cyclopeptide_exp_spec, 0.3)
# mass_table = {x: count for x, count in amino_acid_masses.items() if count >= 24}
mass_table = {mass: mass for mass, _ in amino_acid_masses.most_common(m)}

mass_ranges = [(m - 0.3, m + 0.3) for m in cyclopeptide_exp_spec[-11:]]  # any of last 11 could be mass of peptide
score_func = lambda s1, s2: score_spectrums(s1, s2, 0.3)
res = sequence_cyclic_peptide(
    cyclopeptide_exp_spec,
    n,
    mass_table,
    score_func,
    mass_ranges,
    25)

all_peptides = []
for mass_range, leader_peptides in res.items():
    for score, peptides in leader_peptides.items():
        all_peptides.extend(peptides)


def max_position_distance(p1: List[N], p2: List[N]) -> N:
    max_idx_dists = []
    for p2_rotated in rotate(p2):
        max_idx_dist = max(abs(aa2 - aa1) for aa1, aa2 in zip(p1, p2_rotated))
        max_idx_dists.append(max_idx_dist)
    return min(max_idx_dists)


all_peptides_smoothed = Counter([HashableList([round(aa, 0) for aa in p]) for p in all_peptides])
peptide_matches = group_peptides_within_tolerance(all_peptides_smoothed, 2.0)
for p, count in sorted(peptide_matches.items(), key=lambda x: x[1], reverse=True):
    print(f'{p} len={len(p)} matches={count} closeness={max_position_distance(p, fake_peptide)}')