from graph.DirectedGraph import Graph
from helpers import AminoAcidUtils

# Exercise Break: Decode the ideal spectrum {0, 57, 114, 128, 215, 229, 316, 330, 387, 444}.

# My answer:
# ---------
# It just walks all possible paths from source to sink, then outputs.
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


print(f'{to_dot(g)}')

found = set()
recursive_walk(0, found)

for v in found:
    v_rev = ''.join(reversed(v))
    if v_rev in found:
        print(f'{v} / {v_rev}')