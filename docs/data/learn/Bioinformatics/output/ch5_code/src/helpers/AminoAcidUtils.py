from typing import Optional, List, Dict

_codon_to_amino_acid = {'AAA': 'K', 'AAC': 'N', 'AAG': 'K', 'AAU': 'N', 'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T',
                        'AGA': 'R', 'AGC': 'S', 'AGG': 'R', 'AGU': 'S', 'AUA': 'I', 'AUC': 'I', 'AUG': 'M', 'AUU': 'I',
                        'CAA': 'Q', 'CAC': 'H', 'CAG': 'Q', 'CAU': 'H', 'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P',
                        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGU': 'R', 'CUA': 'L', 'CUC': 'L', 'CUG': 'L', 'CUU': 'L',
                        'GAA': 'E', 'GAC': 'D', 'GAG': 'E', 'GAU': 'D', 'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A',
                        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G', 'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V',
                        'UAA': '*', 'UAC': 'Y', 'UAG': '*', 'UAU': 'Y', 'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S',
                        'UGA': '*', 'UGC': 'C', 'UGG': 'W', 'UGU': 'C', 'UUA': 'L', 'UUC': 'F', 'UUG': 'L', 'UUU': 'F'}

_amino_acid_to_codons = dict()
for k, v in _codon_to_amino_acid.items():
    _amino_acid_to_codons.setdefault(v, []).append(k)

_amino_acid_to_mass = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113,
                       'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156,
                       'Y': 163, 'W': 186}

_mass_to_amino_acids = dict()
for k, v in _amino_acid_to_mass.items():
    _mass_to_amino_acids.setdefault(v, []).append(k)

_unique_amino_acid_masses_as_dict = dict([(m, m) for m in _amino_acid_to_mass.values()])


def codon_to_amino_acid(rna: str) -> Optional[str]:
    return _codon_to_amino_acid.get(rna)


def amino_acid_to_codons(codon: str) -> Optional[List[str]]:
    return _amino_acid_to_codons.get(codon)


def get_codon_to_amino_acid_table() -> Dict[str, str]:
    return _codon_to_amino_acid.copy()


def get_amino_acid_to_codons_table() -> Dict[str, List[str]]:
    return _amino_acid_to_codons.copy()


def get_amino_acid_to_mass_table() -> Dict[str, int]:
    return _amino_acid_to_mass.copy()


def get_mass_to_amino_acids_table() -> Dict[int, List[str]]:
    return _mass_to_amino_acids.copy()


# intended to be used as a replacement for get_amino_acid_to_mass_table(), because for certain problems we only track
# the masses, not what the actual amino acid was.
def get_unique_amino_acid_masses_as_dict() -> Dict[int, int]:
    return _unique_amino_acid_masses_as_dict.copy()


def mass_sequence_to_amino_acid_sequence_possibilities(mass_chain: List[int]) -> List[List[str]]:
    ret = [[]]
    for m in mass_chain:
        aas = _mass_to_amino_acids[m]
        new_ret = []
        for r in ret:
            for aa in aas:
                r = r.copy()
                r.append(aa)
                new_ret.append(r)
        ret = new_ret
    return ret
