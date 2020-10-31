import sys

from GCSkew import gc_skew

with open('/home/user/Downloads/dataset_240220_6.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]
skew = gc_skew(seq)

min_skew = min(skew)
min_skews = [str(i) for i, s in enumerate(skew) if s == min_skew]


print(f'{" ".join(min_skews)}')