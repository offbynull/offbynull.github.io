from decimal import Decimal
from collections import Counter

from LeaderboardCyclopeptideSequencing import sequence_cyclic_peptide
from SpectrumConvolution import spectrum_convolution

with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

m = 40
n = 1000
cyclic_peptide_experimental_spectrum = [Decimal(w) for w in data.strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case

amino_acid_masses = spectrum_convolution(cyclic_peptide_experimental_spectrum)
top_m_amino_acid_masses = Counter(amino_acid_masses).most_common(m)

mass_table = dict([(mass, mass) for mass, _ in top_m_amino_acid_masses])

leader_peptides = sequence_cyclic_peptide(cyclic_peptide_experimental_spectrum, n, mass_table=mass_table)

ret = ' '.join(['-'.join([str(i) for i in p]) for p in leader_peptides])
print(f'{ret}')