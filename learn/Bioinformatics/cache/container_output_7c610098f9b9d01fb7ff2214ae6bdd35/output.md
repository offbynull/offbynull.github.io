`{bm-disable-all}`[ch4_code/src/EncodePeptide.py](ch4_code/src/EncodePeptide.py) (lines 9 to 26):`{bm-enable-all}`

```python
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
```