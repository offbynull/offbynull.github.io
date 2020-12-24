from random import Random
from typing import List

from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from SequencePeptide_Leaderboard import sequence_peptide
from SequenceTester import SequenceTester
from SpectrumConvolution import spectrum_convolution
from SpectrumConvolutionNoise import spectrum_convolution_noise
from SpectrumScore import score_spectrums
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum, PeptideType
from helpers.AminoAcidUtils import get_unique_amino_acid_masses_as_dict
from helpers.Utils import rotate_left

# Generate a noisy spectrum for a fake peptide
r = Random(1)
fake_peptide = [147, 97, 147, 147, 114, 128, 163, 99, 71, 156]  # mass = 1269
exp_spec = theoretical_spectrum(fake_peptide, PeptideType.CYCLIC, get_unique_amino_acid_masses_as_dict())
exp_spec = [float(w) for w in exp_spec]
# remove 0.2x randomly (but re-add the final mass if it was removed)
fake_peptide_mass = exp_spec[-1]
r.shuffle(exp_spec)
exp_spec = exp_spec[:int(len(exp_spec) * 0.8)]
exp_spec.sort()
if exp_spec[-1] != fake_peptide_mass:
    exp_spec += [fake_peptide_mass]
# add noise
exp_spec = [w + r.uniform(-0.3, 0.3) for w in exp_spec]
# add weight of +1 charge (a single proton)
exp_spec = [w + 1.007 for w in exp_spec]
# add 0.75x junk masses
for i in range(0, int(len(exp_spec) * 0.75)):
    idx = r.randrange(0, len(exp_spec))
    junk_val = exp_spec[idx] + r.uniform(0, 50)
    exp_spec.append(junk_val)
# sort
exp_spec.sort()

m = 30
n = 5000
exp_spec_mass_tolerance = 0.3  # max amount of noise per spectrum entry
estimated_peptide_len = 10  # how long you think the peptide is
estimated_peptide_masses = exp_spec[-11:]  # suspected final cyclopeptide mass is in here
score_backlog = 10  # for peptides to be returned, they need to be within x of the top score

exp_spec = [round(m - 1.007, 1) for m in exp_spec]  # remove mass for +1 charge and round

# run convolution to get possible masses
aa_mass_tolerance = spectrum_convolution_noise(exp_spec_mass_tolerance)
aa_masses = spectrum_convolution(exp_spec, aa_mass_tolerance, round_digits=0)
aa_mass_table = {mass: mass for mass, _ in aa_masses.most_common(m)}


# run leader board to get possible peptides
peptide_mass_noise = experimental_spectrum_peptide_mass_noise(exp_spec_mass_tolerance, estimated_peptide_len)
peptide_mass_candidates = [(m - peptide_mass_noise, m + peptide_mass_noise) for m in estimated_peptide_masses]
testers = sequence_peptide(
    exp_spec,
    aa_mass_table,
    aa_mass_tolerance,
    peptide_mass_candidates,
    PeptideType.CYCLIC,
    score_backlog,
    n
)

# the found peptides are grouped by the mass ranges they were for.
def max_position_distance(p1: List[float], p2: List[float]) -> float:
    max_idx_dists = []
    for p2_rotated in rotate_left(p2):
        max_idx_dist = max(abs(aa2 - aa1) for aa1, aa2 in zip(p1, p2_rotated))
        max_idx_dists.append(max_idx_dist)
    return min(max_idx_dists)


for tester in testers.testers:
    for score, peptides in tester.leader_peptides.items():
        for peptide in peptides:
            theo_spec = SequenceTester.generate_theroetical_spectrum_with_tolerances(
                peptide,
                PeptideType.CYCLIC,
                {aa: aa for aa in peptide},
                aa_mass_tolerance
            )
            score = score_spectrums(exp_spec, theo_spec)
            print(f'{(tester.peptide_min_mass, tester.peptide_max_mass)} -> {peptide} len={len(peptide)}'
                  f' closeness={max_position_distance(peptide, fake_peptide)}'
                  f' mass={sum(peptide)}'
                  f' score={score}')
# For the settings above, the peptide is found. It's one of the best scoring peptides / closest peptides...
# (1263.9468911002136, 1276.5468911002135) -> [114.0, 128.0, 163.0, 99.0, 71.0, 156.0, 147.0, 98.0, 147.0, 147.0] len=10 closeness=1.0 mass=1270.0 score=(65, 57.176851851851886, 0.8796438746438752)