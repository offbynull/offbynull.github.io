from NaiveSpectrumScore import score_spectrums
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide

with open('/home/user/Downloads/dataset_240282_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
cyclopeptide = data[0].strip()
expected_spectrum = [int(m) for m in data[1].strip().split()]

cp_spectrum = theoretical_spectrum_of_cyclic_peptide(cyclopeptide)

score = score_spectrums(cp_spectrum, expected_spectrum)
print(f'{score}')