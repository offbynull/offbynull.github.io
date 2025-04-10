from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from PeptideType import PeptideType
from SequencePeptide_Leaderboard import sequence_peptide
from SequenceTester import SequenceTester
from SpectrumConvolution import spectrum_convolution
from SpectrumScore import score_spectrums

# This attempts to sequence the peptide for the a real noisy spectrum while the other file  attempts to sequence a
# peptide from a generated (fake) noisy spectrum. This one (real) gets close to sequencing the real peptide while the
# 2nd one (generated) can sequence the peptide pretty convincingly. My belief is that the 1st one fails to sequence
# because it isn't a noisy spectrum in the sense of random noise, but rather it's either...
#
#  * parts of multiple spectrums from multiple different but similar peptides blended together.
#  * a noisy spectrum with specific parts replaced so as to make the leaderboard algorithm converge in an incorrect
#    direction for a few iterations, causing the subpeptides for the correct direction to get trimmed out.
#
# In either case, the leaderboard algorithm starts getting pushed towards bad subpeptides by the time it expands to the
# ~5-6th position. So much so that the good subpeptides sink to rank > 200000. At that rank, there's no way those good
# subpeptide make it past the leaderboard's trim.
#
# So how do you deal with this problem? My guess is that you need to either ...
#
# * expand the trim limit to capture sub-peptides that fall behind. Doing so adds a lot of computational burden and
#   returns way too many peptides.
# * come up with a new scoring/trimming mechanism for leaderboard. I tried to measure both how many masses match between
#   the theoretical spectrum and the experimental spectrum and how closely those matches align (because this is noisy
#   data). That didn't help too much.
# * expand more than 1 amino acid at a time (I have yet to try this).
# * bootstrap a list of items into the leadboard before starting the algorithm. Since we know that the real spectrum is
#   for a Tyrocidine, you could bootstrap with subpeptides of the Tyrocidine you found earlier in this chapter. I tried
#   this and it works very well (see LeaderboardBootstrap version) -- with a n of 500 and the initial leaderboard
#   bootstrapped with subpeptides from Tyrocidine B and B1 (both sequenced during previous problems for this chapter).
# * at each expand/trim step, try searching for subpeptides in the leaderboard that may be stitchable together and if
#   they score well on stitching then keep them around or use them to influence your next expansion (I have yet to try
#   this). Since both subpeptides may be part of the same full peptide (because they score well), stitching them may be
#   a viable option.
# * try genetic algorithms instead of leaderboard (I tried this along with stitching and while it does start to converge
#   on high scoring subpeptides, it runs into the same problem is that those high-scoring subpeptides lead to bad
#   overall peptides and it easily gets stuck in local optima).
with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
exp_spec = [float(w) for w in data.strip().split()]
exp_spec.sort()  # should be sorted already, but just in case

m = 15
n = 27000
exp_spec_mass_tolerance = 0.3  # max amount of noise per spectrum entry
estimated_peptide_len = 10  # how long you think the peptide is
estimated_peptide_masses = exp_spec[-5:]  # suspected final cyclopeptide mass is in here
score_backlog = 10  # for peptides to be returned, they need to be within x of the top score

exp_spec = [round(m - 1.007, 1) for m in exp_spec]  # remove mass for +1 charge and round

# run convolution to get possible masses
aa_mass_tolerance = exp_spec_mass_tolerance * 2
aa_masses = spectrum_convolution(exp_spec, aa_mass_tolerance, round_digits=0)
aa_mass_table = {mass: mass for mass, _ in aa_masses.most_common(m)}


# run leader board to get possible peptides
peptide_mass_noise = experimental_spectrum_peptide_mass_noise(exp_spec_mass_tolerance, estimated_peptide_len)
peptide_mass_candidates = [(m - peptide_mass_noise, m + peptide_mass_noise) for m in estimated_peptide_masses]
peptide_mass_candidates.append((peptide_mass_candidates[-1][1], peptide_mass_candidates[-1][1] + 20.0))  # add an extra mass range -- the real mass for this peptide is larger than the mass ranges derived above
testers = sequence_peptide(
    exp_spec,
    aa_mass_table,
    aa_mass_tolerance,
    peptide_mass_candidates,
    PeptideType.CYCLIC,
    score_backlog,
    n
)


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
                  f' mass={sum(peptide)}'
                  f' score={score}')

# During one of my previous iterations of this problem, I solved the peptide for the real noisy spectrum by happenstance
# + knowing that the peptide was similar to the other Tyrocidines solved earlier in this chapter. The algorithm above
# returns lots of peptides, one of which gets very very close to the answer (one position has an incorrect amino acid).
# I've been trying to reverse engineer what it is that's causing the real spectrum to be so problematic vs the generated
# spectrum (which this algorithm solves no problem) and my thoughts are that it isn't a real spectrum but a spectrum
# that's been intentionally engineered to throw off the leaderboard algorithm (because causing the student grief forces
# them to try new things / learn more vs easily solving the problem).
#
# The peptide for the real spectrum is 99 128 113 147 97 147 147 114 128 163, which is Tyrocidine A according to
# http://bix.ucsd.edu/nrp