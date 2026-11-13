from BreakpointGraph import BreakpointGraph

with open('/home/user/Downloads/dataset_240324_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
p_list1 = [[int(x) for x in s.split(' ')] for s in lines[0][1:-1].split(')(')]
p_list2 = [[int(x) for x in s.split(' ')] for s in lines[1][1:-1].split(')(')]


bg = BreakpointGraph(p_list1, p_list2)
cycles = bg.get_red_blue_cycles()

block_count = len(bg.node_to_blue_edges) // 2  # number of synteny blocks is number of nodes / 2
cycle_count = len(cycles)

print(f'{block_count - cycle_count}')