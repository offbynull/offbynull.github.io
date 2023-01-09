import json
from collections import Counter
from typing import TypeVar

from graph.DirectedGraph import Graph
from helpers.Utils import slide_window



# Exercise Break: Show that the vertical edge connecting (i, l) to (i, k), where k is a deletion state, should be
# assigned weight equal to transition(l, k).
#
# I CANT REPRODUCE THE GRAPH HERE.

# MY ANSWER
# ---------
# Show it how? I'm not sure what this is even asking for. The graph has been re-ordered such that a deletion-to-deletion
# transition moves downward in the same column. It should have the same weight as the incorrect example previously where
# it was moving across columns, but it's just moving downward now because it isn't emitting a symbol (the book says its
# illegal for a viterbi graph to have edges that move to the next column but emit nothing).
