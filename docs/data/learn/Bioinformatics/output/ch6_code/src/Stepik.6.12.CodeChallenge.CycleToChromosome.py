from typing import List

from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240327_5(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
line = lines[0]
cycle = [int(i) for i in line[1:-1].split()]


def cycle_to_chromosome(c: List[int]) -> List[int]:
    p = []
    p_size = len(c) // 2
    for x1, x2, idx in zip(c[::2], c[1::2], range(1, p_size + 1)):
        if x1 < x2:
            p.append(idx)
        else:
            p.append(-idx)
    return p


print(f'({" ".join([f"+{x}" if x > 0 else str(x) for x in cycle_to_chromosome(cycle)])})')
