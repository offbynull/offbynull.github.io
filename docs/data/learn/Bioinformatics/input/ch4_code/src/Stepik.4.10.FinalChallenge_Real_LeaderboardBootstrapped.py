from random import Random
from typing import List

from NoisyLeaderboardCyclopeptideSequencing import sequence_cyclic_peptide
from NoisyScoreSpectrums import theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses, \
    score_spectrums
from NoisySpectrumConvolution import spectrum_convolution
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from Utils import rotate, get_unique_amino_acid_masses_as_dict, slide_window

with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
cyclopeptide_exp_spec = [float(w) for w in data.strip().split()]
cyclopeptide_exp_spec.sort()  # should be sorted already, but just in case

m = 15
n = 27000
noise_tolerance = 0.3  # max amount of noise per spectrum entry
guessed_len = 10  # how long you think the peptide is
score_backlog = 10  # for peptides to be returned, they need to be within x of the top score
possible_total_cyclopeptide_masses = cyclopeptide_exp_spec[-1:]  # suspected final cyclopeptide mass is in here

cyclopeptide_exp_spec = [round(m - 1.007, 1) for m in cyclopeptide_exp_spec]  # remove mass for +1 charge and round

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
init_peptides = [p for p, _ in slide_window([99.0, 128.0, 113.0, 147.0, 97.0, 186.0, 186.0, 114.0, 128.0, 163.0], 6, cyclic=True)]  # bootstrap with tyrocidine D subpeptides
init_peptides = list(filter(lambda x: all([aa in mass_table for aa in x]), init_peptides))  # make sure all amino acids are present
res = sequence_cyclic_peptide(
    cyclopeptide_exp_spec,
    n,
    mass_table,
    mass_ranges,
    aa_mass_tolerance,
    score_backlog,
    init_peptides
)

# The found peptides are grouped by the mass ranges they were for. Shove everything into a single list.
all_peptides = []
for mass_range, peptides in res.items():
    all_peptides.extend(peptides)

# Print out the list -- if this were for fake_peptide, the function below can be used as a heuristic to determine how
# close each returned peptide is to fake_peptide. Showing closeness was useful for debugging the algorithms.
for p in all_peptides:
    p_theo_spec = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, aa_mass_tolerance)
    score = score_spectrums(cyclopeptide_exp_spec, p_theo_spec)
    print(f'{p} len={len(p)} score={score}')


THE REASON WHY THIS IS STILL FAILING IS BECAUSE THE MASS AT EXP_SPEC[-2] ISNT WHAT THE ACTUAL SUM OF THE INTEGER
PEPTIDES ARE. ITS PROBABLY THE NOISEY RESULT (although that mass is actually the mass listed for tyrocidine a on http://bix.ucsd.edu/nrp/tyrA/index.html).
THE TRUE SUM IS 1283.0 -- THIS IS WHY NOTHING IS CAPTURING THE TRUE AA SEQUENCE