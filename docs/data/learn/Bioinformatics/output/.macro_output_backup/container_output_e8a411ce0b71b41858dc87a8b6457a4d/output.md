`{bm-disable-all}`[ch2_code/src/MedianStringSearch.py](ch2_code/src/MedianStringSearch.py) (lines 8 to 33):`{bm-enable-all}`

```python
# The name is slightly confusing. What this actually does...
#   For each dna string:
#     Find the k-mer with the min hamming distance between the k-mers that make up the DNA string and pattern
#   Sum up the min hamming distances of the found k-mers (equivalent to the motif matrix score)
def distance_between_pattern_and_strings(pattern: str, dnas: List[str]) -> int:
    min_hds = []

    k = len(pattern)
    for dna in dnas:
        min_hd = None
        for dna_kmer, _ in slide_window(dna, k):
            hd = hamming_distance(pattern, dna_kmer)
            if min_hd is None or hd < min_hd:
                min_hd = hd
        min_hds.append(min_hd)
    return sum(min_hds)


def median_string(k: int, dnas: List[str]):
    last_best: Tuple[str, int] = None  # last found consensus string and its score
    for kmer in enumerate_patterns(k):
        score = distance_between_pattern_and_strings(kmer, dnas)  # find score of best motif matrix where consensus str is kmer
        if last_best is None or score < last_best[1]:
            last_best = kmer, score
    return last_best
```