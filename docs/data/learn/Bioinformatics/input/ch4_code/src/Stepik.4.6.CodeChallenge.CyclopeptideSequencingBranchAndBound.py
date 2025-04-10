from PeptideType import PeptideType
from SequencePeptide_Naive_BranchAndBound import sequence_peptide
from helpers.AminoAcidUtils import get_unique_amino_acid_masses_as_dict

with open('/home/user/Downloads/dataset_240281_6(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

cyclic_peptide_experimental_spectrum = [int(w) for w in data.strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case

mass_table = get_unique_amino_acid_masses_as_dict()

final_peptides = sequence_peptide(cyclic_peptide_experimental_spectrum, PeptideType.CYCLIC, mass_table)

ret = ' '.join(['-'.join([str(i) for i in p]) for p in final_peptides])
print(f'{ret}')
