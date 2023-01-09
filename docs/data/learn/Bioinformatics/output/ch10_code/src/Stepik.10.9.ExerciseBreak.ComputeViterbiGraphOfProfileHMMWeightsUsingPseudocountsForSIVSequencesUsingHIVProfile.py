from collections import Counter
from math import log
from typing import TypeVar

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph
from helpers.Utils import slide_window


# Exercise Break: Solve the Sequence Alignment with Profile HMM Problem for the profile HMM you constructed for the
# gp120 multiple alignment reproduced below along with a gp120 protein taken from chimpanzee Simian Immunodeficiency
# Virus (SIV).
#
# VKKLGEQFR-NKTIIFNQPSGGDLEIVMHSFNCGGEFFYCNTTQLFN----------NSTES------DTITL
# VKKLGEQFR-NKTIIFNQPSGGDLEIVMHSFNCGGEFFYCNTTQLFN----------NSTDNG-----DTITL
# VKKLGEQFR-NKTIIFNQPSGGDLEIVMHSFNCGGEFFYCNTTQLFD----------NSTESNN----DTITL
# VDKLREQFGKNKTIIFNQPSGGDLEIVMHTFNCGGEFFYCNTTQLFNSTWNS---TGNGTESYNGQENGTITL
# VDKLREQFGKNKTIIFNQPSGGDLEIVMHTFNCGGEFFYCNTTQLFNSTWNG---TNTT--GLDG--NDTITL
# VDKLREQFGKNKTIIFNQSSGGDLEIVTHTFNCGGEFFYCNTTQLFNSNWTG---NSTE--GLHG--DDTITL
# VKKLGEQFG-NKTIIFNQSSGGGLEIVMHSFNCGGEFFYCNTTQLFNN--TR-----NSTESNNGQGNDTTTL
# VKKLREQFGKNKTIIFKQSSGGDLEIVTHTFNCAGEFFYCNTTQLFNSNWTE-----NSITGLDG--NDTITL
# VGKLREQFGK-KTIIFNQPSGGDLEIVMHSFNCQGEFFYCNTTRLFNSTWDNSTWNSTGKDKENGN-NDTITL

#
# MY ANSWER (Same as the code challenge, just modified to use this new sequence set and symbol set)








E = TypeVar('E')


class StableColumn:
    def __init__(self, elements: list[E]):
        self.elements = elements

    def missing_count(self):
        return sum(1 for e in self.elements if e is None)

    def kept_count(self):
        return sum(1 for e in self.elements if e is not None)

    def is_set(self, row_idx: int):
        return self.elements[row_idx] is not None

    def determine_emission_probabilities(self, symbols: list[E], psuedocount: float):
        total = 0.0
        counts = {s: 0.0 for s in symbols}
        for e in self.elements:
            if e is None:
                continue
            counts[e] += 1
            total += 1
        ret = {k: v / total for k, v in counts.items()}
        ret_total = 0.0
        for e, v in ret.items():
            ret[e] += psuedocount
            ret_total += ret[e]
        return {k: v / ret_total for k, v in ret.items()}

    def __str__(self):
        return f'{self.__class__.__name__}: {self.elements}'

    def __format__(self, format_spec):
        return str(self)

    def __repr__(self):
        return str(self)


class UnstableColumns:
    def __init__(self, elements: list[E]):
        self.rows = [[e] for e in elements]

    def attach_column(self, elements: list[E]):
        for i, e in enumerate(elements):
            self.rows[i].append(e)

    def row_set_count(self, row_idx: int):
        ret = 0
        for e in self.rows[row_idx]:
            if e is not None:
                ret += 1
        return ret

    def is_set(self, row_idx: int):
        return self.row_set_count(row_idx) > 0

    def determine_emission_probabilities(self, symbols: list[E], psuedocount: float):
        total = 0.0
        counts = {s: 0.0 for s in symbols}
        for row in self.rows:
            for e in row:
                if e is None:
                    continue
                counts[e] += 1
                total += 1
        ret = {k: v / total for k, v in counts.items()}
        ret_total = 0.0
        for e, v in ret.items():
            ret[e] += psuedocount
            ret_total += ret[e]
        return {k: v / ret_total for k, v in ret.items()}


class ThresholdedAlignment:
    def __init__(self, threshold: float, sequences: list[list[E]], gap_symbol: E):
        self.row_count = len(sequences)
        columns = []
        self.elements_per_row = len(sequences[0])
        for i in range(self.elements_per_row):
            column_elements = [None if s[i] == gap_symbol else s[i] for s in sequences]
            gapped_count = sum(1 for e in column_elements if e is None)
            gapped_perc = gapped_count / self.row_count
            if gapped_perc >= threshold:
                if columns and isinstance(columns[-1], UnstableColumns):
                    columns[-1].attach_column(column_elements)
                else:
                    columns.append(UnstableColumns(column_elements))
            else:
                columns.append(StableColumn(column_elements))
        self.threshold = threshold
        self.columns = columns
        self.col_count = len(columns)
        self.stable_col_count = sum(1 for c in self.columns if isinstance(c, StableColumn))

    def determine_node_path(self, row_idx: int):
        last1 = None
        last2 = None
        last_i = -1
        for data in self.determine_node_path_raw(row_idx):
            if len(data) == 3:
                i, c1, id1 = data
                if last1 is None:
                    yield -1, None, c1, 'S', id1
                last1 = id1, c1
                last2 = id1, c1
            elif len(data) == 5:
                i, c1, c2, id1, id2 = data
                if last1 is None:
                    yield -1, None, c1, 'S', id1
                yield i, c1, c2, id1, id2
                last1 = id1, c1
                last2 = id2, c2
                last_i = i
            else:
                raise ValueError('???')
        yield last_i + 1, last2[1], None, last2[0], 'E'

    def determine_node_path_raw(self, row_idx: int):
        node_idx = 0
        for (c1, c2), i in slide_window(ta.columns, 2):
            if isinstance(c1, StableColumn) and isinstance(c2, StableColumn):
                if c1.is_set(row_idx) and c2.is_set(row_idx):
                    yield i, c1, c2, f'M{node_idx + 1}', f'M{node_idx + 2}'
                elif c1.is_set(row_idx) and not c2.is_set(row_idx):
                    yield i, c1, c2, f'M{node_idx + 1}', f'D{node_idx + 2}'
                elif not c1.is_set(row_idx) and c2.is_set(row_idx):
                    yield i, c1, c2, f'D{node_idx + 1}', f'M{node_idx + 2}'
                elif not c1.is_set(row_idx) and not c2.is_set(row_idx):
                    yield i, c1, c2, f'D{node_idx + 1}', f'D{node_idx + 2}'
                node_idx += 1
            elif isinstance(c1, StableColumn) and isinstance(c2, UnstableColumns):
                if c2.is_set(row_idx):
                    if c1.is_set(row_idx):
                        yield i, c1, c2, f'M{node_idx + 1}', f'I{node_idx + 1}'
                    elif not c1.is_set(row_idx):
                        yield i, c1, c2, f'D{node_idx + 1}', f'I{node_idx + 1}'
                elif i < len(self.columns) - 2:  # c2 will not be set in this block
                    c3 = self.columns[i + 2]
                    if isinstance(c1, StableColumn) and isinstance(c2, UnstableColumns) and isinstance(c3, StableColumn):
                        if c1.is_set(row_idx) and not c2.is_set(row_idx) and c3.is_set(row_idx):
                            yield i, c1, c3, f'M{node_idx + 1}', f'M{node_idx + 2}'
                        elif not c1.is_set(row_idx) and not c2.is_set(row_idx) and not c3.is_set(row_idx):
                            yield i, c1, c3, f'D{node_idx + 1}', f'D{node_idx + 2}'
                        elif not c1.is_set(row_idx) and not c2.is_set(row_idx) and c3.is_set(row_idx):
                            yield i, c1, c3, f'D{node_idx + 1}', f'M{node_idx + 2}'
                        elif c1.is_set(row_idx) and not c2.is_set(row_idx) and not c3.is_set(row_idx):
                            yield i, c1, c3, f'M{node_idx + 1}', f'D{node_idx + 2}'
                else:  # c2 will not be set in this block and there is no third column to read (SPECIAL CASE: ending with an unstable column)
                    if c1.is_set(row_idx):
                        yield i, c1, f'M{node_idx + 1}'
                    elif not c1.is_set(row_idx):
                        yield i, c1, f'D{node_idx + 1}'
                node_idx += 1
            elif isinstance(c1, UnstableColumns) and isinstance(c2, StableColumn):
                if c1.row_set_count(row_idx) > 1:
                    yield i, c1, c1, f'I{node_idx}', f'I{node_idx}'
                if c1.is_set(row_idx):
                    if c2.is_set(row_idx):
                        yield i, c1, c2, f'I{node_idx}', f'M{node_idx + 1}'
                    else:
                        yield i, c1, c2, f'I{node_idx}', f'D{node_idx + 1}'
                else: # c1 will not be set in this block (SPECIAL CASE: starting with an unstable column)
                    if c2.is_set(row_idx):
                        yield i, c2, f'M{node_idx + 1}'
                    elif not c2.is_set(row_idx):
                        yield i, c2, f'D{node_idx + 1}'
            elif isinstance(c1, UnstableColumns) and isinstance(c2, UnstableColumns):
                raise ValueError('Bad state -- should never happen')















emitted_seq = 'RLELGDYKLVEITPIGLAPTNVKRYTTGGTSRNKR'
sequences = '''
VKKLGEQFR-NKTIIFNQPSGGDLEIVMHSFNCGGEFFYCNTTQLFN----------NSTES------DTITL
VKKLGEQFR-NKTIIFNQPSGGDLEIVMHSFNCGGEFFYCNTTQLFN----------NSTDNG-----DTITL
VKKLGEQFR-NKTIIFNQPSGGDLEIVMHSFNCGGEFFYCNTTQLFD----------NSTESNN----DTITL
VDKLREQFGKNKTIIFNQPSGGDLEIVMHTFNCGGEFFYCNTTQLFNSTWNS---TGNGTESYNGQENGTITL
VDKLREQFGKNKTIIFNQPSGGDLEIVMHTFNCGGEFFYCNTTQLFNSTWNG---TNTT--GLDG--NDTITL
VDKLREQFGKNKTIIFNQSSGGDLEIVTHTFNCGGEFFYCNTTQLFNSNWTG---NSTE--GLHG--DDTITL
VKKLGEQFG-NKTIIFNQSSGGGLEIVMHSFNCGGEFFYCNTTQLFNN--TR-----NSTESNNGQGNDTTTL
VKKLREQFGKNKTIIFKQSSGGDLEIVTHTFNCAGEFFYCNTTQLFNSNWTE-----NSITGLDG--NDTITL
VGKLREQFGK-KTIIFNQPSGGDLEIVMHSFNCQGEFFYCNTTRLFNSTWDNSTWNSTGKDKENGN-NDTITL
'''.strip().split()
sequences = [list(s) for s in sequences]
symbols = list('ARNDCEQGHILKMFPSTWYV')
threshold = 0.4
pseudocount = 0.01
ta = ThresholdedAlignment(threshold, sequences, '-')
# print(f'{list(ta.determine_node_path(0))}')
# print(f'{list(ta.determine_node_path(1))}')
# print(f'{list(ta.determine_node_path(2))}')
# print(f'{list(ta.determine_node_path(3))}')
# print(f'{list(ta.determine_node_path(4))}')


class NodeData:
    def __init__(self):
        self.visit_count = 0
        self.col = None

    def __str__(self):
        return f'{self.visit_count}'

    def __format__(self, format_spec):
        return str(self)


class EdgeData:
    def __init__(self):
        self.visit_count = 0
        self.transition_probability = 0.0

    def __str__(self):
        return f'{self.visit_count} ({self.transition_probability})'

    def __format__(self, format_spec):
        return str(self)


g_hmm = Graph()
# Add all nodes
g_hmm.insert_node('S', NodeData())
g_hmm.insert_node('I0', NodeData())
for col_idx in range(ta.stable_col_count):
    g_hmm.insert_node(f'I{col_idx + 1}', NodeData())
    g_hmm.insert_node(f'M{col_idx + 1}', NodeData())
    g_hmm.insert_node(f'D{col_idx + 1}', NodeData())
g_hmm.insert_node('E', NodeData())
# Connect all Is to itself
for col_idx in range(ta.stable_col_count + 1):
    n_id = f'I{col_idx}'
    e_id = n_id, n_id
    g_hmm.insert_edge(e_id, n_id, n_id, EdgeData())
# Connect outgoing from I0
n_from_id = f'I0'
n_to_id = f'D1'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
n_from_id = f'I0'
n_to_id = f'M1'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
# Connect all outgoing Ds, Ms, and Is > 0
for col_idx in range(1, ta.stable_col_count + 1):
    if col_idx < ta.stable_col_count:
        n_from_id = f'D{col_idx}'
        n_to_id = f'D{col_idx + 1}'
        e_id = n_from_id, n_to_id
        g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
        n_from_id = f'D{col_idx}'
        n_to_id = f'M{col_idx + 1}'
        e_id = n_from_id, n_to_id
        g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
        n_from_id = f'M{col_idx}'
        n_to_id = f'M{col_idx + 1}'
        e_id = n_from_id, n_to_id
        g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
        n_from_id = f'M{col_idx}'
        n_to_id = f'D{col_idx + 1}'
        e_id = n_from_id, n_to_id
        g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
        n_from_id = f'I{col_idx}'
        n_to_id = f'M{col_idx + 1}'
        e_id = n_from_id, n_to_id
        g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
        n_from_id = f'I{col_idx}'
        n_to_id = f'D{col_idx + 1}'
        e_id = n_from_id, n_to_id
        g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
    n_from_id = f'D{col_idx}'
    n_to_id = f'I{col_idx}'
    e_id = n_from_id, n_to_id
    g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
    n_from_id = f'M{col_idx}'
    n_to_id = f'I{col_idx}'
    e_id = n_from_id, n_to_id
    g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
# Connect from S
n_from_id = f'S'
n_to_id = f'I0'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
n_from_id = f'S'
n_to_id = f'M1'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
n_from_id = f'S'
n_to_id = f'D1'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
# Connect to E
n_from_id = f'I{ta.stable_col_count}'
n_to_id = f'E'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
n_from_id = f'M{ta.stable_col_count}'
n_to_id = f'E'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
n_from_id = f'D{ta.stable_col_count}'
n_to_id = f'E'
e_id = n_from_id, n_to_id
g_hmm.insert_edge(e_id, n_from_id, n_to_id, EdgeData())

# Set visit counts on nodes
for row_idx in range(ta.row_count):
    for _, col_from, col_to, n_from_id, n_to_id in ta.determine_node_path(row_idx):
        g_hmm.get_node_data(n_from_id).col = col_from
        g_hmm.get_node_data(n_to_id).col = col_to
        g_hmm.get_node_data(n_from_id).visit_count += 1
        e_id = n_from_id, n_to_id
        g_hmm.get_edge_data(e_id).visit_count += 1

# Calculate transition probabilities on edges
for n_id in g_hmm.get_nodes():
    n_data = g_hmm.get_node_data(n_id)
    for _, _, _, e_data in g_hmm.get_outputs_full(n_id):
        if n_data.visit_count != 0:
            e_data.transition_probability = e_data.visit_count / n_data.visit_count

# Add psuedocounts to transition probabilities
for n_id in g_hmm.get_nodes():
    total = 0.0
    for e_id, _, _, e_data in g_hmm.get_outputs_full(n_id):
        e_data.transition_probability += 0.01
        total += e_data.transition_probability
    for e_id, _, _, e_data in g_hmm.get_outputs_full(n_id):
        e_data.transition_probability = e_data.transition_probability / total


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


# print(f'{to_dot(g_hmm)}')


def gen_viterbi_step(
        g_viterbi: Graph,
        g_hmm: Graph,
        n_from_id: tuple[str, str] | None,
        n_to_id: tuple[str, str],
        emitted_seq: list[str],
        emitted_seq_i: int
):
    hmm_n_from_id, viterbi_n_from_id = (None, None) if n_from_id is None else n_from_id
    hmm_n_to_id, viterbi_n_to_id = n_to_id
    if emitted_seq_i == len(emitted_seq) or hmm_n_to_id == 'E':
        return
    if not g_viterbi.has_node(viterbi_n_to_id):
        g_viterbi.insert_node(viterbi_n_to_id)
    if viterbi_n_from_id is not None:
        if not g_viterbi.has_edge((viterbi_n_from_id, viterbi_n_to_id)):
            if g_hmm.get_in_degree(hmm_n_from_id) == 0:
                transition_probability = 1.0 / g_hmm.get_out_degree(hmm_n_from_id)
            else:
                transition_probability = g_hmm.get_edge_data((hmm_n_from_id, hmm_n_to_id)).transition_probability
            emission_probabilities = {s: pseudocount for s in symbols}
            if not (hmm_n_to_id.startswith('D') or hmm_n_to_id.startswith('E')):  # It can't emit anything if it's a deletion state, start or end
                emission_probabilities = {s: 1.0 / len(symbols) for s in symbols}
                col = g_hmm.get_node_data(hmm_n_to_id).col
                if col is not None:
                    emission_probabilities.update(
                        col.determine_emission_probabilities(symbols, pseudocount)
                    )
            emitted_symbol = emitted_seq[emitted_seq_i]
            weight = transition_probability * emission_probabilities[emitted_symbol]
            g_viterbi.insert_edge(
                (viterbi_n_from_id, viterbi_n_to_id),
                viterbi_n_from_id,
                viterbi_n_to_id,
                weight
            )
        else:
            return
    for next_hmm_e_id, _, next_hmm_n_to_id, next_hmm_e_data in g_hmm.get_outputs_full(hmm_n_to_id):
        next_emitted_seq_i = emitted_seq_i
        if not next_hmm_n_to_id.startswith('D'):
            next_emitted_seq_i += 1
        next_n_from_id = hmm_n_to_id, viterbi_n_to_id
        next_n_to_id = next_hmm_n_to_id, f'{next_hmm_n_to_id}_{next_emitted_seq_i}'
        gen_viterbi_step(
            g_viterbi,
            g_hmm,
            next_n_from_id,
            next_n_to_id,
            emitted_seq,
            next_emitted_seq_i
        )


def gen_viterbi(g_hmm: Graph, emitted_seq: list[str]):
    g_viterbi = Graph()
    gen_viterbi_step(g_viterbi, g_hmm, None, ('S', 'S'), emitted_seq, -1)
    viterbi_leaf_nodes = list(g_viterbi.get_leaf_nodes())
    g_viterbi.insert_node('E')
    for viterbi_n_from_id in viterbi_leaf_nodes:
        viterbi_n_to_id = 'E'
        g_viterbi.insert_edge(
            (viterbi_n_from_id, viterbi_n_to_id),
            viterbi_n_from_id,
            viterbi_n_to_id,
            1.0
        )
    return g_viterbi


g_viterbi = gen_viterbi(g_hmm, emitted_seq)

for e in list(g_viterbi.get_edges()):
    weight = g_viterbi.get_edge_data(e)
    log_weight = 0.0 if weight == 0.0 else log(weight)
    g_viterbi.update_edge_data(e, log_weight)

FindMaxPath_DPBacktrack.populate_weights_and_backtrack_pointers(
    g_viterbi,
    'S',
    lambda n, w, e: g_viterbi.update_node_data(n, (w, e)),
    lambda n: g_viterbi.get_node_data(n),
    lambda e: g_viterbi.get_edge_data(e),
)
final_weight, _ = g_viterbi.get_node_data('E')
edges = FindMaxPath_DPBacktrack.backtrack(
    g_viterbi,
    'E',
    lambda n_id: g_viterbi.get_node_data(n_id)
)
alignment = []
for e in edges:
    to_node = g_viterbi.get_edge_to(e)
    alignment.append(to_node)
alignment = alignment[:-1]  # snip off sink node
print(f'{" ".join(alignment)}')
print(f'{final_weight}')
print(f'{to_dot(g_viterbi)}')

print(f'{" ".join(x.split("_")[0] for x in alignment)}')