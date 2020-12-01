from helpers.AminoAcidUtils import codon_to_amino_acid

with open('/home/user/Downloads/dataset_240277_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]

protein_seq = ''
for codon in zip(*[iter(seq)]*3):
    codon_str = ''.join(codon)
    protein_seq += codon_to_amino_acid(codon_str)
protein_seq = protein_seq.replace('*', '')  # remove stop markers
print(protein_seq)