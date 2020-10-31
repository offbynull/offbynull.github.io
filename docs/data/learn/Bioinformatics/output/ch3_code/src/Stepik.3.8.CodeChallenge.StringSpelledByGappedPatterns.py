from Kdmer import Kdmer
from ReadPair import ReadPair

with open('/home/user/Downloads/dataset_240266_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()


lines = data.split('\n')
lines = [l.strip() for l in lines]  # get rid of whitespace
lines = [l for l in lines if len(l) > 0]  # get rid of empty li
k, d = [int(s) for s in lines[0].split(' ')]
splits = [tuple(s.split('|', maxsplit=2)) for s in lines[1:]]

kdmers = [Kdmer(k1, k2, d) for k1, k2 in splits]
readpairs = [ReadPair(kdmer) for kdmer in kdmers]

genome = readpairs[0].stitch(readpairs)
print(f'{genome}')