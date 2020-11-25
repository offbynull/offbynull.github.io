from typing import List

from NoisyMassesLeaderboardCyclopeptideSequencing import sequence_cyclic_peptide
from NoisyMassesScoreSpectrums import theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses, \
    score_spectrums
from NoisySpectrumConvolution import spectrum_convolution
from Utils import rotate


with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
cyclopeptide_exp_spec = [float(w) for w in data.strip().split()]
cyclopeptide_exp_spec.sort()  # should be sorted already, but just in case

m = 30
n = 1000
noise_tolerance = 0.3  # max amount of noise per spectrum entry
guessed_len = 10  # how long you think the peptide is
allowable_trailing = 25  # for peptides to be returned, they need to be within x of the top score
possible_total_cyclopeptide_masses = cyclopeptide_exp_spec[:-11]  # suspected final cyclopeptide mass is in here


# r = Random(1)
# fake_peptide = [147, 97, 147, 147, 114, 128, 163, 99, 71, 156]
# cyclopeptide_exp_spec = theoretical_spectrum_of_cyclic_peptide(fake_peptide, mass_table=get_unique_amino_acid_masses_as_dict())
# cyclopeptide_exp_spec = [float(w) for w in cyclopeptide_exp_spec]
# # remove 0.2x randomly (but re-add the final mass if it was removed)
# fake_peptide_mass = cyclopeptide_exp_spec[-1]
# r.shuffle(cyclopeptide_exp_spec)
# cyclopeptide_exp_spec = cyclopeptide_exp_spec[:int(len(cyclopeptide_exp_spec) * 0.8)]
# cyclopeptide_exp_spec.sort()
# if cyclopeptide_exp_spec[-1] != fake_peptide_mass:
#     cyclopeptide_exp_spec += [fake_peptide_mass]
# # add noise
# cyclopeptide_exp_spec = [w + r.uniform(-0.3, 0.3) for w in cyclopeptide_exp_spec]
# # add weight of +1 charge (a single proton)
# cyclopeptide_exp_spec = [w + 1.007 for w in cyclopeptide_exp_spec]
# # add 2.0x junk masses
# for i in range(0, int(len(cyclopeptide_exp_spec) * 0.75)):
#     idx = r.randrange(0, len(cyclopeptide_exp_spec))
#     junk_val = cyclopeptide_exp_spec[idx] + r.uniform(0, 50)
#     cyclopeptide_exp_spec.append(junk_val)
# # sort
# cyclopeptide_exp_spec.sort()
#
# m = 30
# n = 1000
# noise_tolerance = 0.3  # max amount of noise per spectrum entry
# guessed_len = 10  # how long you think the peptide is
# allowable_trailing = 25  # for peptides to be returned, they need to be within x of the top score
# possible_total_cyclopeptide_masses = cyclopeptide_exp_spec[:-11]  # suspected final cyclopeptide mass is in here


# remove mass for +1 charge and round
cyclopeptide_exp_spec = [round(m - 1.007, 1) for m in cyclopeptide_exp_spec]

# run convolution to get possible masses
#   - Why noisy_tolerance * 2? because each mass in the noisy spectrum is +/-rand(0, noisy_tolerance). Imagine you have
#     a mass spec device adds up to 0.3 in noise to the spectrum. That means that each mass in the spectrum has
#     +/-rand(0, 0.3) added to it. If a spectrum from that device measured 1000 as 999.7 (-0.3 noise) and 1057 as 1057.3
#     (+0.3 noise), then the convolution would return 1057.3-999.7=57.6 vs the non-noisy convolution 1057-1000=57.
#     There's 0.6 difference, which is noisy_tolerance * 2.
#   - Each returned mass is mapped to the number of masses in range m -/+ (noisy_tolerance * 2) where m is the mass.
aa_mass_tolerance = noise_tolerance * 2
aa_masses = spectrum_convolution(cyclopeptide_exp_spec, aa_mass_tolerance, round_digits=0)
mass_table = {mass: mass for mass, _ in aa_masses.most_common(m)}

# run leader board spectrum
#   - Since the spectrum has false masses. Any of last x elements could be mass of peptide. I used x=11, but it could
#     even be more than 11.
#   - Because this is noisy data, you're looking for a mass within some tolerance rather than an exact mass. That range
#     is determined by the amino acid masses calculated above. Specifically, a correctly identified amino acid mass
#     could be up to -/+(noisy_tolerance * 2) away from what it actually is. When that amino acid mass is used to
#     generate the theoretical spectrum that gets scored against the experimental spectrum, that amino acid mass's noise
#     will propagate throughout the masses in the theoretical spectrum. If more than one amino acid masses have noise,
#     the noise in the theoretical spectrum compounds. So, the range used encompasses everything from where all amino
#     acids have -(noisy_tolerance * 2) to all amino acids have +(noisy_tolerance * 2) for some guessed peptide length
#     (I guessed a length of 10).
mass_ranges = [(m - (aa_mass_tolerance * guessed_len), m + (aa_mass_tolerance * guessed_len)) for m in possible_total_cyclopeptide_masses]
res = sequence_cyclic_peptide(
    cyclopeptide_exp_spec,
    n,
    mass_table,
    mass_ranges,
    noise_tolerance * 2,
    allowable_trailing
)

# The found peptides are grouped by the mass ranges they were for. Shove everything into a single list.
all_peptides = []
for mass_range, peptides in res.items():
    all_peptides.extend(peptides)


# Print out the list -- if this were for fake_peptide, the function below can be used as a heuristic to determine how
# close each returned peptide is to fake_peptide. Showing closeness was useful for debugging the algorithms.
def max_position_distance(p1: List[float], p2: List[float]) -> float:
    max_idx_dists = []
    for p2_rotated in rotate(p2):
        max_idx_dist = max(abs(aa2 - aa1) for aa1, aa2 in zip(p1, p2_rotated))
        max_idx_dists.append(max_idx_dist)
    return min(max_idx_dists)


import sys
sys.stdout = open('output.log', 'w')

for p in all_peptides:
    p_theo_spec = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, noise_tolerance * 2)
    score = score_spectrums(cyclopeptide_exp_spec, p_theo_spec)
    print(f'{p} len={len(p)} score={score}')
    # print(f'{p} len={len(p)} closeness={max_position_distance(p, fake_peptide)} score={score}')