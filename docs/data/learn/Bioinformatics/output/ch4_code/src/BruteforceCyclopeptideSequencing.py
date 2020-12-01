from typing import List, Optional, Dict, TypeVar

from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table
from helpers.HashableCollections import HashableList

T = TypeVar('T')


def sequence_cyclic_peptide(
        cyclopeptide_experimental_spectrum: List[int],
        mass_table: Optional[Dict[T, int]] = None
) -> List[List[T]]:
    if mass_table is None:
        mass_table = get_amino_acid_to_mass_table()

    cyclopeptide_experimental_spectrum.sort()  # Just in case -- it should already be sorted
    cyclopeptide_experimental_mass = cyclopeptide_experimental_spectrum[-1]

    candidate_peptides = {HashableList()}
    final_peptides = []
    while len(candidate_peptides) > 0:
        new_candidate_peptides = set()
        for p in candidate_peptides:
            for m in mass_table.keys():
                new_p = HashableList(p)
                new_p.append(m)
                new_p_mass = sum([mass_table[aa] for aa in new_p])
                if new_p_mass == cyclopeptide_experimental_mass \
                        and theoretical_spectrum_of_cyclic_peptide(new_p) == cyclopeptide_experimental_spectrum:
                    final_peptides.append(new_p)
                elif new_p_mass < cyclopeptide_experimental_mass:
                    new_candidate_peptides.add(new_p)
        candidate_peptides = new_candidate_peptides

    return final_peptides


if __name__ == '__main__':
    mass_table = get_amino_acid_to_mass_table()
    actual_seq = sequence_cyclic_peptide(
        theoretical_spectrum_of_cyclic_peptide('NQE', mass_table=mass_table),
        mass_table=mass_table
    )
    print(f'{actual_seq}')
