from decimal import Decimal
from collections import Counter
from math import floor, ceil

from FuzzyLeaderboardCyclopeptideSequencing import sequence_cyclic_peptide
from SpectrumConvolution import spectrum_convolution

with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

m = 100
n = 1000
cyclic_peptide_experimental_spectrum = [round(float(w), 1) for w in data.strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case

amino_acid_masses = spectrum_convolution(cyclic_peptide_experimental_spectrum)
amino_acid_masses = [round(m, 0) for m in amino_acid_masses]
top_m_amino_acid_masses = Counter(amino_acid_masses).most_common(m)

mass_table = dict([(mass, mass) for mass, _ in top_m_amino_acid_masses])

leader_peptides = sequence_cyclic_peptide(cyclic_peptide_experimental_spectrum, n, mass_table=mass_table, score_tolerance=2.0, mass_tolerance=100.0)

ret = '\n'.join([' '.join([str(i) for i in p]) for p in leader_peptides])
print(f'{ret}')