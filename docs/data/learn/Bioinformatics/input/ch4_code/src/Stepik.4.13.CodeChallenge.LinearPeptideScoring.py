from SpectrumScore_NoNoise import score_spectrums
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum, PeptideType
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table

with open('/home/user/Downloads/dataset_240288_1.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
peptide = data[0].strip()
experimental_spectrum = [int(m) for m in data[1].strip().split()]
theoretical_spectrum = theoretical_spectrum(list(peptide), PeptideType.LINEAR, get_amino_acid_to_mass_table())

print(f'{score_spectrums(theoretical_spectrum, experimental_spectrum)}')