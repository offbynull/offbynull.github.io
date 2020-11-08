from ScoreSpectrums import score_spectrums, top_n_peptides_including_last_place_ties
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from Utils import get_unique_amino_acid_masses_as_dict

with open('/home/user/Downloads/dataset_240282_8(3).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
n = int(data[0].strip())
cyclic_peptide_experimental_spectrum = [int(w) for w in data[1].strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case
cyclic_peptide_experimental_mass = cyclic_peptide_experimental_spectrum[-1]

mass_table = get_unique_amino_acid_masses_as_dict()


leaderboard = [[]]
leader_peptide = next(iter(leaderboard))
while len(leaderboard) > 0:
    # Branch
    new_leaderboard = []
    for p in leaderboard:
        for m in mass_table:
            new_p = p[:]
            new_p.append(m)
            new_leaderboard.append(new_p)
    leaderboard = new_leaderboard
    # Bound
    new_leaderboard = []
    for p in leaderboard:
        p_mass = sum(p)
        if p_mass > cyclic_peptide_experimental_mass:
            continue
        elif p_mass == cyclic_peptide_experimental_mass:
            p_theoretical_spectrum = theoretical_spectrum_of_cyclic_peptide(p, mass_table=mass_table)
            p_score = score_spectrums(p_theoretical_spectrum, cyclic_peptide_experimental_spectrum)
            leader_theoretical_spectrum = theoretical_spectrum_of_cyclic_peptide(leader_peptide, mass_table=mass_table)
            leader_score = score_spectrums(leader_theoretical_spectrum, cyclic_peptide_experimental_spectrum)
            if p_score > leader_score:
                leader_peptide = p
        new_leaderboard.append(p)
    leaderboard = new_leaderboard
    leaderboard = top_n_peptides_including_last_place_ties(
        leaderboard,
        cyclic_peptide_experimental_spectrum,
        n,
        mass_table=mass_table)

ret = '-'.join([str(i) for i in leader_peptide])
print(f'{ret}')