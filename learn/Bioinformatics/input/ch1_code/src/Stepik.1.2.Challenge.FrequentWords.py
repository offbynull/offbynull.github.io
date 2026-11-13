from CountASequencesKmers import kmer_frequency

with open('/home/user/Downloads/dataset_240214_13(2).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]
k = int(lines[1])

counter = kmer_frequency(seq, k)
top_count = max(counter.values())
most_frequent_kmers = [kmer for kmer, count in counter.items() if count == top_count]

print(f'{" ".join(most_frequent_kmers)}')