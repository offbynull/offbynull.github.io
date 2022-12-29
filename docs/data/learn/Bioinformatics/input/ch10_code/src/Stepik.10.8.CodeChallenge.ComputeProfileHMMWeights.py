from collections import defaultdict, Counter
from enum import Enum
from itertools import product

from graph import DirectedGraph
from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator
from helpers.Utils import slide_window

with open('/home/user/Downloads/test.txt') as f:
    lines = f.read().splitlines(keepends=False)
threshold = float(lines[0])
symbols = set(lines[2].split())
sequences = lines[4:]

col_count = len(sequences[0])
row_count = len(sequences)

# Ignore any column where gaps appear with a frequency more than threshold. If non-gaps exist in those ignored columns,
# it's treated as "inserted" data into the sequence.
class ColumnType(Enum):
    INSERTION = 'INSERTION'
    ELEMENT = 'ELEMENT'

class Column:
    def __init__(self, type: ColumnType, elements: list[str]):
        self.type = type
        self.elements = elements

columns = []
for i in range(col_count):
    column_elements = [s[i] for s in sequences]
    gapped_count = sum(1 for ch in column_elements if ch == '-')
    gapped_perc = gapped_count / row_count
    if gapped_perc >= threshold:
        column_type = ColumnType.INSERTION
    else:
        column_type = ColumnType.ELEMENT
    if len(columns) == 0:
        if column_type == ColumnType.INSERTION:
            columns.append(Column(ColumnType.INSERTION, column_elements))
        else:
            columns.append(Column(ColumnType.INSERTION, ['' for s in sequences]))
            columns.append(Column(ColumnType.ELEMENT, column_elements))
    else:
        if columns[-1].type == ColumnType.INSERTION and column_type == ColumnType.INSERTION:
            columns[-1].elements = [old + new for old, new in zip(columns[-1].elements, column_elements)]
        elif columns[-1].type == ColumnType.ELEMENT and column_type == ColumnType.ELEMENT:
            columns.append(Column(ColumnType.INSERTION, ['' for s in sequences]))
            columns.append(Column(ColumnType.ELEMENT, column_elements))
        elif columns[-1].type == ColumnType.INSERTION and column_type == ColumnType.ELEMENT:
            columns.append(Column(ColumnType.ELEMENT, column_elements))
        elif columns[-1].type == ColumnType.ELEMENT and column_type == ColumnType.INSERTION:
            columns.append(Column(ColumnType.INSERTION, column_elements))
if columns[-1].type == ColumnType.ELEMENT:
    columns.append(Column(ColumnType.INSERTION, ['' for s in sequences]))


# Create graph nodes and edges
class NodeData:
    def __init__(self, elements: list[str]):
        self.elements = elements
        self.visit_count = 0
        self.to_counts = Counter()

    def __str__(self):
        return f'{self.elements}\\n{self.visit_count}'

    def __format__(self, format_spec):
        return str(self)

g = Graph()
next_insert_n_id = 0
next_element_n_id = 1
for c in columns:
    if c.type == ColumnType.INSERTION:
        g.insert_node(f'I{next_insert_n_id}', NodeData(c.elements))
        next_insert_n_id += 1
    else:
        g.insert_node(f'M{next_element_n_id}', NodeData(c.elements))
        g.insert_node(f'D{next_element_n_id}', NodeData(c.elements))
        next_element_n_id += 1

for i in range(next_insert_n_id - 1):
    n_from_id, n_to_id = f'I{i}', f'I{i}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
    n_from_id, n_to_id = f'I{i}', f'I{i + 1}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
    n_from_id, n_to_id = f'I{i}', f'D{i + 1}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
    n_from_id, n_to_id = f'I{i}', f'M{i + 1}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
for i in range(1, next_element_n_id - 1):
    n_from_id, n_to_id = f'D{i}', f'D{i + 1}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
    n_from_id, n_to_id = f'M{i}', f'M{i + 1}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
    n_from_id, n_to_id = f'D{i}', f'I{i}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
    n_from_id, n_to_id = f'M{i}', f'I{i}'
    g.insert_edge(
        (n_from_id, n_to_id),
        n_from_id,
        n_to_id
    )
g.insert_node('S')
for n_id in {'I0', 'D1', 'M1'}:
    if g.has_node(n_id):
        g.insert_edge(
            ('S', n_id),
            'S',
            n_id
        )
g.insert_node('E')
for n_id in {f'I{next_insert_n_id - 1}', f'D{next_element_n_id - 1}', f'M{next_element_n_id - 1}'}:
    if g.has_node(n_id):
        g.insert_edge(
            (n_id, 'E'),
            n_id,
            'E'
        )

# Walk each sequenced through the graph to determine how many times each node gets walked into by the sequences
for r in range(row_count):
    next_insert_n_id = 0
    next_element_n_id = 1
    for i, c in enumerate(columns):
        # Count how many times each sequence visits
        if c.type == ColumnType.INSERTION:
            if c.elements[r] != '' and set(c.elements[r]) != {'-'}:  # if not empty and not all dashes
                n_current_id = f'I{next_insert_n_id}'
                non_gap_count = sum(1 for ch in c.elements[r] if ch != '-')
                if non_gap_count > 1:
                    g.get_node_data(n_id).visit_count += 2
                elif non_gap_count == 1:
                    g.get_node_data(n_id).visit_count += 1
            next_insert_n_id += 1
        elif c.type == ColumnType.ELEMENT:
            if c.elements[r] != '-':
                n_current_id = f'M{next_element_n_id}'
                g.get_node_data(n_current_id).visit_count += 1
            else:
                n_current_id = f'D{next_element_n_id}'
                g.get_node_data(n_current_id).visit_count += 1
            next_element_n_id += 1


TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT
TODO: THIS IS TOO CONFUSING. START ABSTRACTING THINGS OUT


def to_dot(g: DirectedGraph.Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = g.get_nodes()
    for n in nodes:
        data = g.get_node_data(n)
        ret += f'"{n}" [label="{n}\\n{data}"]\n'  # \\n{g.get_node_data(n)}
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'"{n1}" -> "{n2}"\n'  # [label="{weight}"]
    ret += '}'
    return ret


print(f'{to_dot(g)}')
