from SpectrumScore_NoNoise import score_spectrums
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum, PeptideType
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table

with open('/home/user/Downloads/dataset_240282_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
cyclopeptide = data[0].strip()
expected_spectrum = [int(m) for m in data[1].strip().split()]

cp_spectrum = theoretical_spectrum(list(cyclopeptide), PeptideType.CYCLIC, get_amino_acid_to_mass_table())

score = score_spectrums(cp_spectrum, expected_spectrum)
print(f'{score}')