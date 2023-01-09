import math
from collections import Counter
from itertools import product
from math import log
from typing import TypeVar

from find_max_path import FindMaxPath_DPBacktrack
from graph.DirectedGraph import Graph
from helpers.Utils import slide_window


# Challenge Problem: Using the Pfam HMM for gp120 (constructed from a seed alignment of just 24 gp120 proteins),
# construct alignments of all known gp120 proteins and identify the “most diverged” gp120 sequence.

HMM HAS BEEN DOWNLOADED TO A FILE CALLED GP120.HMM

FIGURE OUT HOW TO READ THIS AND APPLY IT

ALSO, GO BACK TO 10.12 (JUST AFTER THE CHALLENGE PROBLEM) AND 10.13 AND 10.14 AND FIGURE THOSE SECTIONS OUT AND DO THE MISSING CHALLENGE PROBLEMS.