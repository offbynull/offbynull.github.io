from typing import List

from helpers.AminoAcidUtils import codon_to_amino_acid
from helpers.DnaUtils import dna_reverse_complement, dna_to_rna
from helpers.Utils import split_to_size, slide_window


# MARKDOWN
def encode_peptide(dna: str) -> str:
    rna = dna_to_rna(dna)
    protein_seq = ''
    for codon in split_to_size(rna, 3):
        codon_str = ''.join(codon)
        protein_seq += codon_to_amino_acid(codon_str)
    return protein_seq


def encode_peptides_all_readingframes(dna: str) -> List[str]:
    ret = []
    for dna_ in (dna, dna_reverse_complement(dna)):
        for rf_start in range(3):
            rf_end = len(dna_) - ((len(dna_) - rf_start) % 3)
            peptide = encode_peptide(dna_[rf_start:rf_end])
            ret.append(peptide)
    return ret
# MARKDOWN


def find_peptide_encodings_in_dna(dna: str, peptide: str) -> List[str]:
    ret = []
    k = len(peptide) * 3
    for kmer, _ in slide_window(dna, k):
        dna_kmer = kmer
        dna_kmer_rc = dna_reverse_complement(kmer)
        found = False
        for test_dna in (dna_kmer, dna_kmer_rc):
            test_peptide = encode_peptide(test_dna)
            if ''.join(test_peptide) == peptide:
                found = True
                break
        if found:
            ret.append(kmer)
    return ret


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dna = input().strip()
        peptides = encode_peptides_all_readingframes(dna)
        print(f'Given {dna}, the possible peptide encodings are...', end="\n\n")
        for peptide in peptides:
            peptide = peptide.replace('*', '\\*')  # md escaping
            print(f' * {peptide}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()