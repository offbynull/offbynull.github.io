import lzma

from FindPeptideEncodingInDna import find_peptide_encodings_in_dna

tyrocodine_b1_amino_acid_seq = 'VKLFPWFNQY'
with lzma.open('Bacillus_brevis.txt.xz', mode='rt', encoding='utf-8') as f:
    bacillus_brevis_dna_seq = ''.join(f.read().split())

print(f'{len(find_peptide_encodings_in_dna(bacillus_brevis_dna_seq, tyrocodine_b1_amino_acid_seq))}')
