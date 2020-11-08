from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide

with open('/home/user/Downloads/dataset_240279_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.strip()

spectrum = theoretical_spectrum_of_cyclic_peptide(data)

print(f'{" ".join([str(i) for i in spectrum])}')
