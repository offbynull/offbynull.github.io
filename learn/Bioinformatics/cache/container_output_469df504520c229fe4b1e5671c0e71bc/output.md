`{bm-disable-all}`[ch1_code/src/FindAllDnaKmersWithinHammingDistance.py](ch1_code/src/FindAllDnaKmersWithinHammingDistance.py) (lines 5 to 20):`{bm-enable-all}`

```python
def find_all_dna_kmers_within_hamming_distance(kmer: str, hamming_dist: int) -> set[str]:
    def recurse(kmer: str, hamming_dist: int, output: set[str]) -> None:
        if hamming_dist == 0:
            output.add(kmer)
            return

        for i in range(0, len(kmer)):
            for ch in 'ACTG':
                neighbouring_kmer = kmer[:i] + ch + kmer[i + 1:]
                recurse(neighbouring_kmer, hamming_dist - 1, output)

    output = set()
    recurse(kmer, hamming_dist, output)

    return output
```