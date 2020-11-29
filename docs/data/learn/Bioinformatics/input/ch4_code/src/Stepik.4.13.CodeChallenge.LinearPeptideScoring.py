from ScoreSpectrums import score_spectrums
from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide

with open('/home/user/Downloads/dataset_240288_1.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
peptide = data[0].strip()
experimental_spectrum = [int(m) for m in data[1].strip().split()]
theoretical_spectrum = theoretical_spectrum_of_linear_peptide(peptide)

print(f'{score_spectrums(theoretical_spectrum, experimental_spectrum)}')