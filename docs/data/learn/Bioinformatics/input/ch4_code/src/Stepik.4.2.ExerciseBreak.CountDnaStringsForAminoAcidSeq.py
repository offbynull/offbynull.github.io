from Utils import amino_acid_to_codons

amino_acid_seq = 'VKLFPWFNQY'
count = 1
for ch in amino_acid_seq:
    vals = amino_acid_to_codons(ch)
    print(f'{ch} = {vals}')
    count *= len(vals)
print(f'{count}')

