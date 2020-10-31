from FindPeptideEncodingInDna import find_peptide_encodings_in_dna

with open('/home/user/Downloads/dataset_240277_7.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dna_seq = lines[0]
amino_acid_seq = lines[1]


for seq in find_peptide_encodings_in_dna(dna_seq, amino_acid_seq):
    print(f'{seq}')
