from typing import List

from BreakpointGraph import BreakpointGraph

with open('/home/user/Downloads/dataset_240324_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
from_p_list = [[int(x) for x in s.split(' ')] for s in lines[0][1:-1].split(')(')]
to_p_list = [[int(x) for x in s.split(' ')] for s in lines[1][1:-1].split(')(')]


def p_list_to_output(x: List[List[int]]):
    ret = ''
    for p in x:
        ret += '('
        ret += ' '.join(('+' if i > 0 else '') + str(i) for i in p)
        ret += ')'
    return ret


bg = BreakpointGraph(
    from_p_list,
    to_p_list
)
print(p_list_to_output(bg.get_red_permutations()))
while True:
    next_blue_edge_to_break_on = bg.find_blue_edge_in_non_trivial_cycle()
    if next_blue_edge_to_break_on is None:
        break
    bg.apply_2break(next_blue_edge_to_break_on)
    print(p_list_to_output(bg.get_red_permutations()))
