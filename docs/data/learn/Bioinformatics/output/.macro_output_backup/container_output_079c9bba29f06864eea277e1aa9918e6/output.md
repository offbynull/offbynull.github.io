`{bm-disable-all}`[ch4_code/src/DecodePeptide.py](ch4_code/src/DecodePeptide.py) (lines 8 to 27):`{bm-enable-all}`

```python
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
```