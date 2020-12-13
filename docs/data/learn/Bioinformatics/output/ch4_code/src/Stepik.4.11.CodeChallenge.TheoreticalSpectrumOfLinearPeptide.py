from PrefixSumTheoreticalSpectrum import theoretical_spectrum, PeptideType
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table

with open('/home/user/Downloads/dataset_240286_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.strip()

spectrum = theoretical_spectrum(list(data), PeptideType.LINEAR, get_amino_acid_to_mass_table())

print(f'{" ".join([str(i) for i in spectrum])}')
