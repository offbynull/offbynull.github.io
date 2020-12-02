from typing import List

from helpers.AminoAcidUtils import codon_to_amino_acid
from helpers.DnaUtils import dna_reverse_complement


# MARKDOWN
def encode_peptide(dna: str) -> str:
    rna = dna.replace('T', 'U')
    protein_seq = ''
    for codon in zip(*[iter(rna)] * 3):
        codon_str = ''.join(codon)
        protein_seq += codon_to_amino_acid(codon_str)
    return protein_seq


def encode_all_possible_peptides(dna: str) -> List[str]:
    ret = []
    for dna_ in (dna, dna_reverse_complement(dna)):
        for rf_offset in range(3):
            peptide = encode_peptide(dna_[rf_offset:])
            ret.append(peptide)
    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dna = input().strip()
        peptides = encode_all_possible_peptides(dna)
        print(f'Given {dna}, the possible peptide encodings are...', end="\n\n")
        for peptide in peptides:
            peptide = peptide.replace('*', '\\*')  # md escaping
            print(f' * {peptide}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()