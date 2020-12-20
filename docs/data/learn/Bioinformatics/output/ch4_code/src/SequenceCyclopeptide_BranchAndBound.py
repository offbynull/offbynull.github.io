from typing import List, Optional, Dict, TypeVar

from TheoreticalSpectrum_PrefixSum import theoretical_spectrum, PeptideType
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table
from helpers.HashableCollections import HashableList
from helpers.Utils import contains_all_sorted

T = TypeVar('T')


def sequence_cyclic_peptide(
        cyclopeptide_experimental_spectrum: List[int],
        mass_table: Optional[Dict[T, int]] = None
) -> List[List[T]]:
    if mass_table is None:
        mass_table = get_amino_acid_to_mass_table()

    cyclopeptide_experimental_spectrum.sort()  # Just in case -- it should already be sorted
    cyclopeptide_experimental_mass = cyclopeptide_experimental_spectrum[-1]

    candidate_peptides = [[]]
    final_peptides = []
    while len(candidate_peptides) > 0:
        # Branch
        new_candidate_peptides = set()
        for p in candidate_peptides:
            for m in mass_table:
                new_p = HashableList(p)
                new_p.append(m)
                new_candidate_peptides.add(new_p)
        candidate_peptides = new_candidate_peptides
        # Bound
        removal_set = set()
        for p in candidate_peptides:
            p_mass = sum([mass_table[aa] for aa in p])
            if p_mass == cyclopeptide_experimental_mass:
                if theoretical_spectrum(p, PeptideType.CYCLIC, mass_table) == cyclopeptide_experimental_spectrum:
                    final_peptides.append(p)
                removal_set.add(p)
            elif not contains_all_sorted(
                    theoretical_spectrum(p, PeptideType.LINEAR, mass_table),
                    cyclopeptide_experimental_spectrum):
                removal_set.add(p)
        candidate_peptides -= removal_set

    return final_peptides


if __name__ == '__main__':
    mass_table = get_amino_acid_to_mass_table()
    actual_seq = sequence_cyclic_peptide(
        theoretical_spectrum(list('NQELNQEA'), PeptideType.CYCLIC, mass_table),
        mass_table=mass_table
    )
    print(f'{actual_seq}')