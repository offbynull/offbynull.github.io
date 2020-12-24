from PeptideType import PeptideType
from SequencePeptide_Naive_Leaderboard import sequence_peptide

with open('/home/user/Downloads/dataset_240283_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
n = int(data[0].strip())
cyclic_peptide_experimental_spectrum = [int(w) for w in data[1].strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case

mass_table = dict([(i, i) for i in range(57, 200 + 1)])

leader_peptides = sequence_peptide(
    cyclic_peptide_experimental_spectrum,
    PeptideType.CYCLIC,
    cyclic_peptide_experimental_spectrum[-1],
    mass_table,
    n
)

ret = '\n'.join(['-'.join([str(i) for i in p]) for p in leader_peptides])
print(f'{ret}')