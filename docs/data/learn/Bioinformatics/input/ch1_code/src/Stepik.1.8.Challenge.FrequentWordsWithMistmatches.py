from CountASequencesKmersWithMismatches import kmer_frequency_with_mismatches

with open('/home/user/Downloads/dataset_240221_9.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
seq = lines[0]
k, min_hamming_dist = [int(x) for x in lines[1].split()]

counter = kmer_frequency_with_mismatches(seq, k, min_hamming_dist)
top_count = max(counter.values())
most_frequent_kmers = [kmer for kmer, count in counter.items() if count == top_count]

print(f'{" ".join(most_frequent_kmers)}')