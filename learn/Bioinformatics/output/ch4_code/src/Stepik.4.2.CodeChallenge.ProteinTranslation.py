from EncodePeptide import encode_peptide
from helpers.DnaUtils import rna_to_dna

with open('/home/user/Downloads/dataset_240277_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]

print(f'{encode_peptide(rna_to_dna(seq)).replace("*", "")}')