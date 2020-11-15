from collections import Counter
from random import Random
from typing import List, Tuple

from CycleCheck import count_rotation_occurrences
from FuzzyLeaderboardCyclopeptideSequencing2 import sequence_cyclic_peptide
from FuzzyScoreSpectrums2 import score_spectrums
from SpectrumConvolution import spectrum_convolution
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from Utils import get_unique_amino_acid_masses_as_dict, N

# with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
#     data = f.read()
# cyclic_peptide_experimental_spectrum = [float(w) for w in data.strip().split()]
# cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case


r = Random(1)
cyclic_peptide_experimental_spectrum = theoretical_spectrum_of_cyclic_peptide([147, 147, 97, 99, 113, 114], mass_table=get_unique_amino_acid_masses_as_dict())
cyclic_peptide_experimental_spectrum = [float(w) for w in cyclic_peptide_experimental_spectrum]
cyclic_peptide_experimental_spectrum = [w + r.uniform(-0.3, 0.3) for w in cyclic_peptide_experimental_spectrum]  # add noise
cyclic_peptide_experimental_spectrum = [w + 1.007 for w in cyclic_peptide_experimental_spectrum]  # add weight of +1 charge (a single proton)
for i in range(0, len(cyclic_peptide_experimental_spectrum) * 2):
    idx = r.randrange(0, len(cyclic_peptide_experimental_spectrum))
    junk_val = cyclic_peptide_experimental_spectrum[idx] + r.uniform(0, 50)
    cyclic_peptide_experimental_spectrum.append(junk_val)
cyclic_peptide_experimental_spectrum.sort()

m = 60
n = 1000

cyclic_peptide_experimental_spectrum = [round(m - 1.007, 1) for m in cyclic_peptide_experimental_spectrum]  # remove mass for +1 charge and round

amino_acid_masses = spectrum_convolution(cyclic_peptide_experimental_spectrum)
amino_acid_masses = [round(m, 1) for m in amino_acid_masses]  # remove fp rounding errors
amino_acid_masses.sort()
top_m_amino_acid_masses = Counter(amino_acid_masses).most_common(m)
mass_table = dict([(mass, mass) for mass, _ in top_m_amino_acid_masses])


for i in range(0, 16):
    print(f'{i}')

    s = cyclic_peptide_experimental_spectrum if i == 0 else cyclic_peptide_experimental_spectrum[:-i]

    score_func = lambda s1, s2: score_spectrums(s1, s2, 0.3)
    leader_peptides = sequence_cyclic_peptide(
        s,
        n,
        mass_table,
        score_func,
        0.3,
        6)

    for score, peptides in leader_peptides.items():
        for p, count in count_rotation_occurrences(peptides):
            if count == 1:
                continue
            p_str = ' '.join([str(i) for i in p])
            print(f'{p_str}   len={len(p)} / score={score} / count={count}')