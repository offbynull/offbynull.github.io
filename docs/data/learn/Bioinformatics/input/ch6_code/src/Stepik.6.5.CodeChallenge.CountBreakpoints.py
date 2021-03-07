from typing import List

from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240320_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
signed_permutation = [int(i) for i in lines[0].split()]


def count_bp(p: List[int]) -> int:
    # instead of 1 to n, the chapter now says to make it 0 to n+1 where 0 and n+1 are implied AND fixed into place
    p = [0] + p + [len(p) + 1]
    return sum(0 if x1 + 1 == x2 else 1 for (x1, x2), _ in slide_window(p, 2))


print(f'{count_bp(signed_permutation)}')
