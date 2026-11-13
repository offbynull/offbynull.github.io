from FindMostProbableKmerUsingProfileMatrix import find_most_probable_kmer_using_profile_matrix

with open('/home/user/Downloads/dataset_240241_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dna = lines[0]
k = int(lines[1])
profile_matrix = {
    'A': [float(f) for f in lines[2].split(' ')],
    'C': [float(f) for f in lines[3].split(' ')],
    'G': [float(f) for f in lines[4].split(' ')],
    'T': [float(f) for f in lines[5].split(' ')]
}

found = find_most_probable_kmer_using_profile_matrix(profile_matrix, dna)
print(f'{found[0]}')
