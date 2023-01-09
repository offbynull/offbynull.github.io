from graph.DirectedGraph import Graph
from helpers import AminoAcidUtils
from helpers.Utils import slide_window

# Exercise Break: REDCA is one possible peptide that explains some but not all of the masses in the spectrum shown in
# the figure below, which has false and missing masses. Can you find another peptide that explains even more masses in
# this spectrum?

# My answer:
# ---------
# This is the same as the DecodEIdealSpectrumCorrectly exercise break from the last chapter, but maybe instead of
# checking that the found pepetide's spectrum matches the original spectrum, it's better to check if its within some
# threshold? (e.g. +/- 5 masses).
#
# I've updated the code as such and ran it below. These seem like a good candidate:
#
# REDCA (extra=1 missing=8)  <-- original (8 masses missing)
# IGDFAA (extra=2 missing=7) <-- only 7 masses missing
# IGDDCA (extra=2 missing=7) <-- only 7 masses missing
orig_spectrum = [0, 71, 103, 113, 142, 156, 170, 174, 250, 285, 289, 400, 403, 413, 432, 503, 574]

g = Graph()
for w in orig_spectrum:
    g.insert_node(w)

aa_to_mass = AminoAcidUtils.get_amino_acid_to_mass_table()
mass_to_aas = AminoAcidUtils.get_mass_to_amino_acids_table()
max_mass = max(mass_to_aas)

for i, mass1 in enumerate(orig_spectrum):
    for j in range(i+1, len(orig_spectrum)):
        mass2 = orig_spectrum[j]
        diff = mass2 - mass1
        if diff > max_mass:
            break
        aas = mass_to_aas.get(diff, None)
        if aas is None:
            continue
        aa = aas[0]
        g.insert_edge(f'{mass1}->{mass2}', mass1, mass2, aa)


def recursive_walk(node, output: set[str], prefix=None):
    if prefix is None:
        prefix = []
    if g.get_out_degree(node) == 0:
        output.add(''.join(prefix))
        return
    for e_id, n_from, n_to, e_data in g.get_outputs_full(node):
        prefix.append(e_data)
        recursive_walk(n_to, output, prefix)
        prefix.pop()


def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = g.get_nodes()
    for n in nodes:
        data = g.get_node_data(n)
        ret += f'"{n}" [label="{n}\\n{data}"]\n'  # \\n{g.get_node_data(n)}
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        ret += f'"{n1}" -> "{n2}" [label="{data}"]\n'  # [label="{weight}"]
    ret += '}'
    return ret


def to_spectrum(peptide: str):
    spectrum = {0}
    for k in range(len(peptide) + 1): # ADD PREFIX AND SUFFIX
        weight = sum(aa_to_mass[ch] for ch in peptide[0:k])
        spectrum.add(weight)
        weight = sum(aa_to_mass[ch] for ch in peptide[k:])
        spectrum.add(weight)
    return sorted(spectrum)


def check_spectrum_within_limits(peptide: str):
    peptide_spectrum = set(to_spectrum(peptide))
    _orig_spectrum = set(orig_spectrum)
    _orig_spectrum.difference(peptide_spectrum)
    extra_masses = peptide_spectrum - _orig_spectrum
    missing_masses = _orig_spectrum - peptide_spectrum
    return len(extra_masses), len(missing_masses)


print(f'{to_dot(g)}')

found = set()
recursive_walk(0, found)

while found:
    v = found.pop()
    extra, missing = check_spectrum_within_limits(v)
    print(f'{v} ({extra=} {missing=})')