from typing import List

from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240327_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
line = lines[0]
signed_permutation = [int(i) for i in line[1:-1].split()]


def chromosome_to_cycle(p: List[int]) -> List[int]:
    ret = []
    for i, chromosome in enumerate(p):
        i += 1
        if chromosome > 0:
            ret.append(2*i - 1)
            ret.append(2*i)
        else:
            ret.append(2*i)
            ret.append(2*i - 1)
    return ret


print(f'({" ".join([str(x) for x in chromosome_to_cycle(signed_permutation)])})')
