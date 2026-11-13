from Read import Read

with open('/home/user/Downloads/dataset_240256_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
kmers = lines[:]
kmers = [l.strip() for l in kmers] # get rid of whitespace
kmers = [l for l in kmers if len(l) > 0] # get rid of empty lines

reads = [Read(kmer) for kmer in kmers]

composition = reads[0].stitch(reads)
print(composition)