from graph.DirectedGraph import Graph
from helpers import AminoAcidUtils
from helpers.Utils import slide_window

# Exercise Break: Which masses in the spectrum below does the peptide GGDTN fail to explain?

# My answer:
# ---------
# This is the same as the last exercise, but the last exercise didn't have you do one last required piece: For each
# string given back, you need to calculate the spetrum of that string and ensure it matches up with the original input
# spectrum.
#
# GGDTN fails because its spectrum doesn't include 128, while the original spectrum does. However, the problem is
# claiming that there are 8 of 32 paths in the graph have a matching spectrum. I'm only getting 6. In this case, my
# spectrums only include prefixes and suffixes. I tried including middle chunks but then nothing matches.
orig_spectrum = [0, 57, 114, 128, 215, 229, 316, 330, 387, 444]

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


print(f'{to_dot(g)}')

found = set()
recursive_walk(0, found)

while found:
    v = found.pop()
    v_spectrum = to_spectrum(v)
    v_rev = ''.join(reversed(v))
    found.remove(v_rev)
    print(f'{v} / {v_rev}: {v_spectrum} {v_spectrum == orig_spectrum}')