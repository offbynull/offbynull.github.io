from Read import Read
from ToOverlapGraphHash import to_overlap_graph

with open('/home/user/Downloads/dataset_240256_10(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
dnas = lines[:]
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

reads = [Read(kmer) for kmer in dnas]
overlaps = to_overlap_graph(reads)
for kmer, other_kmers in overlaps.get_all_outputs():
    other_kmers = list(other_kmers)
    if len(other_kmers) == 0:
        continue
    print(f'{kmer} -> {",".join([str(x) for x in other_kmers])}')
