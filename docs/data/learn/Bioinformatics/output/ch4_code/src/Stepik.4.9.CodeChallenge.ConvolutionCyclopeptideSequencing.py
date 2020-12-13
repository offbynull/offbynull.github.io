from collections import Counter

from NaiveLeaderboardCyclopeptideSequencing import sequence_cyclic_peptide
from NaiveSpectrumConvolution import spectrum_convolution

with open('/home/user/Downloads/dataset_240284_7.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
m = int(data[0].strip())
n = int(data[1].strip())
cyclic_peptide_experimental_spectrum = [int(w) for w in data[2].strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case

amino_acid_masses = spectrum_convolution(cyclic_peptide_experimental_spectrum)
top_m_amino_acid_masses = Counter(amino_acid_masses).most_common(m)

mass_table = dict([(m, m) for m, _ in top_m_amino_acid_masses])

leader_peptides = sequence_cyclic_peptide(cyclic_peptide_experimental_spectrum, n, mass_table=mass_table)

ret = '-'.join([str(i) for i in leader_peptides[0]])
print(f'{ret}')