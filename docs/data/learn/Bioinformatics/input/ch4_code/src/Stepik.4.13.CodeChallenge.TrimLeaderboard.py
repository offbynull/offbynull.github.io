from NaiveLeaderboardSequenceCyclopeptide import top_n_peptides_including_last_place_ties
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table

with open('/home/user/Downloads/dataset_240288_3(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
peptides = [list(p) for p in data[0].strip().split()]
experimental_spectrum = [int(m) for m in data[1].strip().split()]
experimental_spectrum.sort()  # just in case -- spectra should be sorted smallest ot largest
top_n = int(data[2].strip())

peptides = top_n_peptides_including_last_place_ties(peptides, experimental_spectrum, top_n, mass_table=get_amino_acid_to_mass_table())

print(f'{" ".join(["".join(p) for p in peptides])}')