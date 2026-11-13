from MotifEnumeration import motif_enumeration

with open('/home/user/Downloads/dataset_240238_8(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0].split()[0])
max_mismatches = int(lines[0].split()[1])
dnas = lines[1:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

motifs = motif_enumeration(dnas, k, max_mismatches)
print(f'{" ".join(motifs)}')