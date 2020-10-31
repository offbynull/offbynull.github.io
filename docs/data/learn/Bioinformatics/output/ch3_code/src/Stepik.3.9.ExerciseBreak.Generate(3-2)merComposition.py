from Utils import slide_window_kd

dna = 'TAATGCCATGGGATGTT'
kdmers = []
for kdmer, _ in slide_window_kd(dna, 3, 2):
    kdmers.append('(' + kdmer.head + '|' + kdmer.dst + ')')

kdmers.sort()
print(f'{" ".join(kdmers)}')