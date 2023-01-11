from graph.DirectedGraph import Graph
from helpers import AminoAcidUtils
from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240417_6.txt') as f:
    lines = f.read().splitlines(keepends=False)

peptide_vector = [int(i) for i in lines[0].split()]

# aa_to_mass = {'X': 4, 'Z': 5}
# mass_to_aas = {5: ['Z'], 4: ['X']}

aa_to_mass = AminoAcidUtils.get_amino_acid_to_mass_table()
mass_to_aas = AminoAcidUtils.get_mass_to_amino_acids_table()


def to_prefix_masses(peptide: str):
    spectrum = set()
    for k in range(1, len(peptide) + 1): # ADD PREFIX AND SUFFIX
        weight = sum(aa_to_mass[ch] for ch in peptide[0:k])
        spectrum.add(weight)
    return sorted(spectrum)


prefix_masses = [i+1 for i, m in enumerate(peptide_vector) if m == 1]
mass = prefix_masses[0]
peptide = '' + mass_to_aas[mass][0]
for (m1, m2), _ in slide_window(prefix_masses, 2):
    mass = m2 - m1
    peptide += mass_to_aas[mass][0]
print(f'{peptide}')
