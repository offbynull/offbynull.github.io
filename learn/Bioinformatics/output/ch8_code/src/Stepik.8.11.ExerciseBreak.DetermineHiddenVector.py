import math
import random
from collections import defaultdict
from math import dist, nan
from statistics import mean

# Exercise Break: Determine the rest of the entries in HiddenVector for Parameters = (0.6, 0.82) and the five sequences
# of coin flips, reproduced below.
#
#                       Data_seq
# H T T T H T T H T H     0.7
# H H H H T H H H H H     0.4
# H T H H H H H T H H     0.9
# H T T T T T H H T T     0.8
# T H H H T H H H T H     0.3

# MY ANSWER
# ---------
# Notes from the chapter up until this exercise and then the code for the calculation
#
#   θ = probability that a single clip results in heads, given n past coin flips
#
#   two coins, each with their own bias: θa and θb  (collectively called parameterS)
#   every n flips, randomly choose one of the two coins -- you don't know which one, only that it might have switched
#
#   e.g. 5 sequences @ n=10 is (0.4,0.9,0.8,0.3,0.7)
#
#   if you knew that θa was used for (0.4,0.3) and θb (0.9,0.8,0.7)...
#     θa = avg(0.4,0.3) = 0.35
#     θb = avg(0.9,0.8,0.7) = 0.89
#
#   in the sequence, represent each time θa as 1 and θb as 0...
#
#     (θa,θb,θb,θa,θb)
#     (1 ,0 ,0 ,1 ,0 )   <-- call this hiddenvector
#
#   θa = sum(d*c for d, c in zip(data_seq, hiddenvector)) / sum(hiddenvector)
#   θb = sum(d*(1-c) for d, c in zip(data_seq, hiddenvector)) / sum(1-c for c in hiddenvector)
#
#   if you know θa,θb,data_seq, you can estimate hiddenvector by looking at the observed flips in each seq and
#   determining if coin A or coin B was more likely to have generated it
#     given θa=0.6, θb=0.82, and data_seq=(0.4,0.9,0.8,0.3,0.7), the probability that ...
#       coin a used to generate 5th entry (0.7) is (θa^7)*(1-θa)^3 = (0.6^7)*(1-0.6)^3   = (0.6^7)*(0.4)^3   = 0.00179
#   	coin b used to generate 5th entry (0.7) is (θb^7)*(1-θb)^3 = (0.82^7)*(1-0.82)^3 = (0.82^7)*(0.18)^3 = 0.00145

prob_a = 0.6
prob_b = 0.82
observed_flips = [
    'HTTTHTTHTH',
    'HHHHTHHHHH',
    'HTHHHHHTHH',
    'HTTTTTHHTT',
    'THHHTHHHTH'
]

for flip_seq in observed_flips:
    h_count = sum(1 for e in flip_seq if e == 'H')
    t_count = sum(1 for e in flip_seq if e == 'T')
    prob_a_was_the_coin = (prob_a ** h_count) * (1 - prob_a) ** t_count
    prob_b_was_the_coin = (prob_b ** h_count) * (1 - prob_b) ** t_count
    print(f'{flip_seq} = {prob_a_was_the_coin=} / {prob_b_was_the_coin=}')