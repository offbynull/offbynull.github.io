from typing import List, TypeVar

from PeptideType import PeptideType
from SpectrumScore_NoNoise import score_spectrums
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table

T = TypeVar('T')


with open('/home/user/Downloads/dataset_240288_3(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
peptides = [list(p) for p in data[0].strip().split()]
experimental_spectrum = [int(m) for m in data[1].strip().split()]
experimental_spectrum.sort()  # just in case -- spectra should be sorted smallest ot largest
top_n = int(data[2].strip())


# Score a set of peptides against a reference spectrum and return the top n (including ties at the end, so it may be end
# up being more than n).
def top_n_peptides_including_last_place_ties(
        peptides: List[List[T]],
        reference_spectrum: List[int],
        n: int,
        mass_table=None
) -> List[List[T]]:
    if len(peptides) == 0:
        return peptides
    spectrums = [theoretical_spectrum(p, PeptideType.LINEAR, mass_table) for p in peptides]
    scores = [score_spectrums(s, reference_spectrum) for s in spectrums]
    sorted_peptide_scores = list(sorted(zip(peptides, scores), key=lambda x: x[1], reverse=True))  # big to small
    # Return first n elements from sorted_peptide_scores, but since we're including ending ties we need to check if the
    # element at n repeats. If it does, include the repeats (the result wil be larger than n).
    for j in range(n + 1, len(sorted_peptide_scores)):
        if sorted_peptide_scores[n][1] > sorted_peptide_scores[j][1]:
            return [p for p, _ in sorted_peptide_scores[:j-1]]
    return [p for p, _ in sorted_peptide_scores]


peptides = top_n_peptides_including_last_place_ties(peptides, experimental_spectrum, top_n, mass_table=get_amino_acid_to_mass_table())

print(f'{" ".join(["".join(p) for p in peptides])}')