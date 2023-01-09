import json
from collections import Counter
from typing import TypeVar

from graph.DirectedGraph import Graph
from helpers.Utils import slide_window



# Exercise Break: Compute the normalized matrix for the matrix below after adding the pseudocount σ = 0.01.
#
#    S   I0  M1  D1  I1  M2  D2  I2  M3  D3  I3  M4  D4  I4  M5  D5  I5  M6  D6  I6  M7  D7  I7  M8  D8  I8  E
# S      x   1   x
# I0     x   x   x
# M1                 x   .8  .2
# D1                 x   x   x
# I1                 x   x   x
# M2                             x   1   x
# D2                             x   x   1
# I2                             x   x   x
# M3                                         x   1   x
# D3                                         x   1   x
# I3                                         x   x   x
# M4                                                     x   .8  .2
# D4                                                     x   x   x
# I4                                                     x   x   x
# M5                                                                 .75 .25 x
# D5                                                                 x   1   x
# I5                                                                 .4 .6  x
# M6                                                                             x   .8  .2
# D6                                                                             x   x   x
# I6                                                                             x   x   x
# M7                                                                                         x   1   x
# D7                                                                                         x   1   x
# I7                                                                                         x   x   x
# M8                                                                                                     x   1
# D8                                                                                                     x   x
# I8                                                                                                     x   x
# E


# MY ANSWER
mat = {
    'S': {'I0': 0.0, 'M1': 1.0, 'D1': 0.0},
    'I0': {'I0': 0.0, 'M1': 0.0, 'D1': 0.0},
    'M1': {'I1': 0.0, 'M2': 0.8, 'D2': 0.2},
    'D1': {'I1': 0.0, 'M2': 0.0, 'D2': 0.0},
    'I1': {'I1': 0.0, 'M2': 0.0, 'D2': 0.0},
    'M2': {'I2': 0.0, 'M3': 1.0, 'D3': 0.0},
    'D2': {'I2': 0.0, 'M3': 0.0, 'D3': 1.0},
    'I2': {'I2': 0.0, 'M3': 0.0, 'D3': 0.0},
    'M3': {'I3': 0.0, 'M4': 1.0, 'D4': 0.0},
    'D3': {'I3': 0.0, 'M4': 1.0, 'D4': 0.0},
    'I3': {'I3': 0.0, 'M4': 0.0, 'D4': 0.0},
    'M4': {'I4': 0.0, 'M5': 0.8, 'D5': 0.2},
    'D4': {'I4': 0.0, 'M5': 0.0, 'D5': 0.0},
    'I4': {'I4': 0.0, 'M5': 0.0, 'D5': 0.0},
    'M5': {'I5': 0.75, 'M6': 0.25, 'D6': 0.0},
    'D5': {'I5': 0.0, 'M6': 1.0, 'D6': 0.0},
    'I5': {'I5': 0.4, 'M6': 0.6, 'D6': 0.0},
    'M6': {'I6': 0.0, 'M7': 0.8, 'D7': 0.2},
    'D6': {'I6': 0.0, 'M7': 0.0, 'D7': 0.0},
    'I6': {'I6': 0.0, 'M7': 0.0, 'D7': 0.0},
    'M7': {'I7': 0.0, 'M8': 1.0, 'D8': 0.0},
    'D7': {'I7': 0.0, 'M8': 1.0, 'D8': 0.0},
    'I7': {'I7': 0.0, 'M8': 0.0, 'D8': 0.0},
    'M8': {'I8': 0.0, 'E': 1.0},
    'D8': {'I8': 0.0, 'E': 0.0},
    'I8': {'I8': 0.0, 'E': 0.0},
    'E': {}
}
for row_id, row in mat.items():
    new_row = {}
    new_row_total = 0.0
    for col_id, value in row.items():
        value = value + 0.01
        new_row[col_id] = value
        new_row_total += value
    if new_row_total != 0.0:
        for col_id, value in row.items():
            new_row[col_id] /= new_row_total
    mat[row_id] = new_row


print(f'{json.dumps(mat, indent=2)}')
