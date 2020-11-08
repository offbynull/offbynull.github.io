from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide

with open('/home/user/Downloads/dataset_240286_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.strip()

spectrum = theoretical_spectrum_of_linear_peptide(data)

print(f'{" ".join([str(i) for i in spectrum])}')
