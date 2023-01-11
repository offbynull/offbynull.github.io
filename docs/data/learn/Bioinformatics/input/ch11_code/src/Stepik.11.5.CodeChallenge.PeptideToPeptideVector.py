from graph.DirectedGraph import Graph
from helpers import AminoAcidUtils
from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240417_5.txt') as f:
    lines = f.read().splitlines(keepends=False)

peptide = lines[0]

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


spec = to_prefix_masses(peptide)
max_mass = max(spec)
peptide_vector = [0 for i in range(max_mass)]
for mass in spec:
    peptide_vector[mass-1] = 1

print(' '.join(f'{i}' for i in peptide_vector))