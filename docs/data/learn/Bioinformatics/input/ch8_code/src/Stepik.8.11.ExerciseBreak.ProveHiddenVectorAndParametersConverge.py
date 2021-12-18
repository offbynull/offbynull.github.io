import math
import random
from collections import defaultdict
from math import dist, nan
from statistics import mean

# As illustrated in the figure below for the initial choice of Parameters = (0.6, 0.82), we repeat these two steps and
# hope that Parameters and HiddenVector are moving closer to the values that maximize Pr(Data|HiddenVector, Parameters),
#
# (Data, ?, Parameters) → (Data, HiddenVector, Parameters)
#                       → (Data, HiddenVector, ?)
#                       → (Data, HiddenVector, Parameters')
#                       → (Data, ?, Parameters')
#                       → (Data, HiddenVector', Parameters')
#                       → ...
#
# Exercise Break: Prove that this process terminates, i.e., that HiddenVector and Parameters eventually stop changing
# between iterations.

# MY ANSWER
# ---------
# I have no idea how to "prove" this. I can barely understand what's happening from all obtuse descriptions and
# formulas. I have a broad mental image of how it possibly converges, but that's it.
