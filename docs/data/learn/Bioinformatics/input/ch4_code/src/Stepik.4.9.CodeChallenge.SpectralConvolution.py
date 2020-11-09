from SpectrumConvolution import spectrum_convolution
from Utils import get_unique_amino_acid_masses_as_dict

with open('/home/user/Downloads/dataset_240284_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

spectrum = [int(w) for w in data.strip().split()]
spectrum.sort()  # should be sorted already, but just in case

mass_table = get_unique_amino_acid_masses_as_dict()

mass_diffs = spectrum_convolution(spectrum, min_mass=1, max_mass=9999999999999999999999999999999999999999999999)

ret = ' '.join([str(i) for i in mass_diffs])
print(f'{ret}')