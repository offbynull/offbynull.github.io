import sys

from ReverseComplementADnaKmer import reverse_complement

#with sys.stdin as f:
with open('/home/user/Downloads/dataset_240215_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]

seq_revcomp = reverse_complement(seq)

print(f'{seq_revcomp}')