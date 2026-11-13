# .--Tights
# |    |
# |    |   ,----->Gloves
# |    v   |
# |  Leotard----->Cape--->Hood
# |    |
# |    v
# |  Shorts----->Belt
# |    |
# |    v
# `->Boots
#
#
# Given the graph above, how many topological orderings does it have? A topological ordering is a 1-dimensional ordering
# of nodes in a directed acyclic graph in which each node is ahead of all of its predecessors / parents. In other words,
# the node is ahead of all other nodes that connect to it.
#
#    For example, the graph ...
#                   ,----> E
#                   |
#                   |
#    A --->  B ---> C ---> D
#            |             ^
#            |             |
#            `-------------'
#    ... the topological order is either [A, B, C, D, E] or [A, B, C, E, D]. Both are correct.
#
#


# I tried thinking about a reasonable way to do this using probabilities and permuations and such, but couldn't. Instead
# I bruteforced the answer. It seems that a lot of people are having trouble with this question because Stepik states
# that the problems only been solved by 3 people so far (5% of tries are correct).
from itertools import permutations

# Don't worry about Tights -> Leotard since they're always needed as the beginning two. Just deal with the rest.
possibilities_after_leotard = []
for p in permutations(["Gloves", "Cape", "Hood", "Shorts", "Boots", "Belt"], 6):
    p = list(p)
    cape_idx = p.index('Cape')
    hood_idx = p.index('Hood')
    if hood_idx < cape_idx:
        continue
    shorts_idx = p.index('Shorts')
    boots_idx = p.index('Boots')
    belt_idx = p.index('Belt')
    if boots_idx < shorts_idx or belt_idx < shorts_idx:
        continue
    possibilities_after_leotard.append(p)

print(f'{possibilities_after_leotard}')
print(f'{len(possibilities_after_leotard)}')
