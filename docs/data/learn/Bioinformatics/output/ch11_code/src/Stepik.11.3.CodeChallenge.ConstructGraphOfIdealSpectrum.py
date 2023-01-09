from graph.DirectedGraph import Graph
from helpers import AminoAcidUtils

with open('/home/user/Downloads/dataset_240415_5.txt') as f:
    lines = f.read().splitlines(keepends=False)

spectrum = [0] + [int(w) for w in lines[0].split()]
spectrum.sort()

g = Graph()
for w in spectrum:
    g.insert_node(w)

aa_to_mass = AminoAcidUtils.get_amino_acid_to_mass_table()
mass_to_aas = AminoAcidUtils.get_mass_to_amino_acids_table()
max_mass = max(mass_to_aas)

for i, mass1 in enumerate(spectrum):
    for j in range(i+1, len(spectrum)):
        mass2 = spectrum[j]
        diff = mass2 - mass1
        if diff > max_mass:
            break
        aas = mass_to_aas.get(diff, None)
        if aas is None:
            continue
        aa = aas[0]
        g.insert_edge(f'{mass1}->{mass2}', mass1, mass2, aa)

for e_id in g.get_edges():
    aa = g.get_edge_data(e_id)
    print(f'{e_id}:{aa}')