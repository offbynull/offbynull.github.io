from FindLocationsOfAKnownKmer import find_kmer_locations

with open('/home/user/Downloads/dataset_240214_6(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]
kmer = lines[1]

arr = find_kmer_locations(seq, kmer)

print(f'{len(arr)}')