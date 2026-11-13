from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from PeptideType import PeptideType
from SequencePeptide_Leaderboard import sequence_peptide
from SequenceTester import SequenceTester
from SpectrumConvolution import spectrum_convolution
from SpectrumScore import score_spectrums
from helpers.Utils import slide_window

with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
exp_spec = [float(w) for w in data.strip().split()]
exp_spec.sort()  # should be sorted already, but just in case

m = 15
n = 15000
exp_spec_mass_tolerance = 0.3  # max amount of noise per spectrum entry
estimated_peptide_len = 10  # how long you think the peptide is
estimated_peptide_masses = exp_spec[-5:]  # suspected final cyclopeptide mass is in here
score_backlog = 10  # for peptides to be returned, they need to be within x of the top score

exp_spec = [round(m - 1.007, 1) for m in exp_spec]  # remove mass for +1 charge and round

# run leader board to get possible peptides
aa_mass_tolerance = exp_spec_mass_tolerance * 2
aa_masses = spectrum_convolution(exp_spec, aa_mass_tolerance, round_digits=0)
aa_mass_table = {mass: mass for mass, _ in aa_masses.most_common(m)}

# run leader board spectrum
peptide_mass_noise = experimental_spectrum_peptide_mass_noise(exp_spec_mass_tolerance, estimated_peptide_len)
peptide_mass_candidates = [(m - peptide_mass_noise, m + peptide_mass_noise) for m in estimated_peptide_masses]
peptide_mass_candidates.append((peptide_mass_candidates[-1][1], peptide_mass_candidates[-1][1] + 20.0))  # add an extra mass range -- the real mass range is larger than all others
  # Bootstrap with peptides tyrocidine B and B1 solved in previous problems for this chapter
init_peptides = []
init_peptides += [p for p, _ in slide_window([99.0, 132.0, 113.0, 147.0, 97.0, 186.0, 147.0, 114.0, 128.0, 163.0], 6, cyclic=True)]
init_peptides += [p for p, _ in slide_window([99.0, 128.0, 113.0, 147.0, 97.0, 186.0, 147.0, 114.0, 128.0, 163.0], 6, cyclic=True)]
init_peptides = list(filter(lambda x: all([aa in aa_mass_table for aa in x]), init_peptides))  # make sure all amino acids in initial are present
testers = sequence_peptide(
    exp_spec,
    aa_mass_table,
    aa_mass_tolerance,
    peptide_mass_candidates,
    PeptideType.CYCLIC,
    score_backlog,
    n,
    init_peptides
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

# The peptide is 99 128 113 147 97 147 147 114 128 163 -- it's in the output in noisy form (e.g. instead of being
# exactly 114 it may be 113 or 115). There was extra code in this project to de-duping the results but it was
# removed for being too slow -- to get the answers to try, you should de-dupe the list (make sure to account for the
# fact that it's cyclic) and normalize each amino acid (e.g. 145.0/146.0/147.0 should actually be 147.0,
# 130.0/129.0/128.0 should actually be 128.0, etc..), remove the ".0" suffix for each amino acid mass, and try each
# item in the answer box until it passes.
#
# A good de-duping data structure may be a trie, where each element may be a single amino acid or an amino acid range
# (e.g. anything between 146 to 147 can probably be grouped together, because it's a single element)
#
# Examples of matches from output...
# (1274.8999999999999, 1294.8999999999999) -> [128.0, 163.0, 99.0, 128.0, 113.0, 147.0, 99.0, 146.0, 145.0, 114.0] len=10 mass=1282.0 score=(46, 34.40122354497363, 0.7478526857602964)
# (1274.8999999999999, 1294.8999999999999) -> [128.0, 163.0, 99.0, 128.0, 113.0, 147.0, 99.0, 145.0, 146.0, 115.0] len=10 mass=1283.0 score=(46, 37.836408730158794, 0.8225306245686694)
# (1274.8999999999999, 1294.8999999999999) -> [128.0, 163.0, 99.0, 128.0, 113.0, 147.0, 98.0, 147.0, 145.0, 114.0] len=10 mass=1282.0 score=(46, 34.692559523809614, 0.7541860766045568)
# (1274.8999999999999, 1294.8999999999999) -> [128.0, 163.0, 99.0, 128.0, 113.0, 147.0, 99.0, 146.0, 146.0, 113.0] len=10 mass=1282.0 score=(46, 34.65816798941806, 0.7534384345525665)
# (1274.8999999999999, 1294.8999999999999) -> [128.0, 163.0, 99.0, 128.0, 113.0, 147.0, 98.0, 147.0, 146.0, 113.0] len=10 mass=1282.0 score=(46, 34.88204365079374, 0.7583052967563857)
# (1274.8999999999999, 1294.8999999999999) -> [128.0, 163.0, 99.0, 128.0, 113.0, 147.0, 98.0, 147.0, 146.0, 114.0] len=10 mass=1283.0 score=(46, 37.22248677248685, 0.809184495054062)
# (1274.8999999999999, 1294.8999999999999) -> [128.0, 163.0, 99.0, 128.0, 113.0, 147.0, 99.0, 145.0, 147.0, 114.0] len=10 mass=1283.0 score=(46, 38.10724206349213, 0.8284183057280898)
# (1274.8999999999999, 1294.8999999999999) -> [163.0, 99.0, 128.0, 113.0, 147.0, 97.0, 146.0, 147.0, 113.0, 130.0] len=10 mass=1283.0 score=(43, 34.796660052910134, 0.8092246523932589)
# (1274.8999999999999, 1294.8999999999999) -> [163.0, 99.0, 128.0, 113.0, 147.0, 97.0, 145.0, 145.0, 114.0, 130.0] len=10 mass=1281.0 score=(47, 33.791369047619185, 0.7189652988855145)
# ...