from typing import List

from helpers.AminoAcidUtils import codon_to_amino_acid
from helpers.DnaUtils import dna_to_rna, dna_reverse_complement
from helpers.Utils import slide_window, split_to_size


def find_peptide_encodings_in_dna(dna: str, amino_acid_seq: str) -> List[str]:
    ret = []
    for kmer, _ in slide_window(dna, len(amino_acid_seq) * 3):
        rna_kmer = dna_to_rna(kmer)
        rna_kmer_rev_comp = dna_to_rna(dna_reverse_complement(kmer))
        found = False
        for rna in [rna_kmer, rna_kmer_rev_comp]:
            amino_acids = [codon_to_amino_acid(codon) for codon in split_to_size(rna, 3)]
            if None in amino_acids:
                continue
            if ''.join(amino_acids) == amino_acid_seq:
                found = True
                break
        if found:
            ret.append(kmer)
    return ret
