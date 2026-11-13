from PeptideType import PeptideType
from SequencePeptide_Naive_Leaderboard import sequence_peptide
from helpers.AminoAcidUtils import get_unique_amino_acid_masses_as_dict

with open('/home/user/Downloads/dataset_240282_10.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
n = int(data[0].strip())
cyclic_peptide_experimental_spectrum = [int(w) for w in data[1].strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case

mass_table = get_unique_amino_acid_masses_as_dict()

leader_peptides = sequence_peptide(
    cyclic_peptide_experimental_spectrum,
    PeptideType.CYCLIC,
    cyclic_peptide_experimental_spectrum[-1],
    mass_table,
    n
)

ret = '\n'.join(['-'.join([str(i) for i in p]) for p in leader_peptides])
print(f'{ret}')