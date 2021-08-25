`{bm-disable-all}`[ch1_code/src/FindRepeating.py](ch1_code/src/FindRepeating.py) (lines 12 to 41):`{bm-enable-all}`

```python
from Utils import slide_window


def count_kmers(data: str, k: int, options: Options = Options()) -> Counter[str]:
    counter = Counter()
    for kmer, i in slide_window(data, k):
        neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer, options.hamming_distance)
        for neighbouring_kmer in neighbourhood:
            counter[neighbouring_kmer] += 1

        if options.reverse_complement:
            kmer_rc = reverse_complement(kmer)
            neighbourhood = find_all_dna_kmers_within_hamming_distance(kmer_rc, options.hamming_distance)
            for neighbouring_kmer in neighbourhood:
                counter[neighbouring_kmer] += 1

    return counter


def top_repeating_kmers(data: str, k: int, options: Options = Options()) -> Set[str]:
    counts = count_kmers(data, k, options)

    _, top_count = counts.most_common(1)[0]

    top_kmers = set()
    for kmer, count in counts.items():
        if count == top_count:
            top_kmers.add((kmer, count))
    return top_kmers
```