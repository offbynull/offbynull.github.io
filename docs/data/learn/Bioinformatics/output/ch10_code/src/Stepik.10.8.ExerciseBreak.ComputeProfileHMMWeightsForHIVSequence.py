from collections import Counter
from typing import TypeVar

from graph.DirectedGraph import Graph
from helpers.Utils import slide_window



# Exercise Break: Construct a profile HMM for the HIV sequences (reproduced below) with θ = 0.35.
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

    def determine_emission_probabilities(self):
        total = 0
        counts = Counter()
        for e in self.elements:
            if e is None:
                continue
            counts[e] += 1
            total += 1
        return {k: v / total for k, v in counts.items()}

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

    def determine_emission_probabilities(self):
        total = 0
        counts = Counter()
        for row in self.rows:
            for e in row:
                if e is None:
                    continue
                counts[e] += 1
                total += 1
        return {k: v / total for k, v in counts.items()}


class ThresholdedAlignment:
    def __init__(self, threshold: float, sequences: list[list[E]], gap_symbol: E):
        self.row_count = len(sequences)
        columns = []
        elem_count_per_row = len(sequences[0])
        for i in range(elem_count_per_row):
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


g = Graph()
for row_idx in range(ta.row_count):
    for _, col_from, col_to, n_from_id, n_to_id in ta.determine_node_path(row_idx):
        if not g.has_node(n_from_id):
            g.insert_node(n_from_id, NodeData())
            g.get_node_data(n_from_id).col = col_from
        if not g.has_node(n_to_id):
            g.insert_node(n_to_id, NodeData())
            g.get_node_data(n_to_id).col = col_to
        g.get_node_data(n_from_id).visit_count += 1

        e_id = n_from_id, n_to_id
        if not g.has_edge(e_id):
            g.insert_edge(e_id, n_from_id, n_to_id, EdgeData())
        g.get_edge_data(e_id).visit_count += 1

for n_id in g.get_nodes():
    n_data = g.get_node_data(n_id)
    for _, _, _, e_data in g.get_outputs_full(n_id):
        e_data.transition_probability = e_data.visit_count / n_data.visit_count


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


potential_n_ids = []
potential_n_ids.append('S')
for i in range(ta.stable_col_count):
    potential_n_ids.append(f'I{i}')
    potential_n_ids.append(f'M{i + 1}')
    potential_n_ids.append(f'D{i + 1}')
potential_n_ids.append(f'I{ta.stable_col_count}')
potential_n_ids.append('E')


print(f'\t', end='')
for n_id in potential_n_ids:
    print(f'{n_id}\t', end='')
print()
for n_from_id in potential_n_ids:
    print(f'{n_from_id}\t', end='')
    for n_to_id in potential_n_ids:
        e_id = n_from_id, n_to_id
        if g.has_node(n_from_id) and g.has_node(n_to_id) and g.has_edge(e_id):
            weight = g.get_edge_data(e_id).transition_probability
        else:
            weight = 0
        print(f'{weight}\t', end='')
    print()


print('--------')


print(f'\t', end='')
for s in symbols:
    print(f'{s}\t', end='')
print()
for n_from_id in potential_n_ids:
    print(f'{n_from_id}\t', end='')
    emission_probabilities = {s: 0 for s in symbols}
    if g.has_node(n_from_id) and not n_from_id.startswith('D'):  # It can't emit anything if it's a deletion state
        col = g.get_node_data(n_from_id).col
        if col is not None:
            emission_probabilities.update(
                col.determine_emission_probabilities()
            )
    for symbol in symbols:
        print(f'{emission_probabilities[symbol]}\t', end='')
    print()
