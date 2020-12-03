from typing import List

from helpers.AminoAcidUtils import amino_acid_to_codons
from helpers.DnaUtils import rna_to_dna


# MARKDOWN
def decode_peptide(peptide: str) -> List[str]:
    def dfs(subpeptide: str, dna: str, ret: List[str]) -> None:
        if len(subpeptide) == 0:
            ret.append(dna)
            return
        aa = subpeptide[0]
        for codon in amino_acid_to_codons(aa):
            dfs(subpeptide[1:], dna + rna_to_dna(codon), ret)
    dnas = []
    dfs(peptide, '', dnas)
    return dnas


def decode_peptide_count(peptide: str) -> int:
    count = 1
    for ch in peptide:
        vals = amino_acid_to_codons(ch)
        count *= len(vals)
    return count
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        peptide = input().strip()
        dnas = decode_peptide(peptide)
        print(f'Given {peptide}, the possible DNA encodings are...', end="\n\n")
        for dna in dnas:
            print(f' * {dna}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()