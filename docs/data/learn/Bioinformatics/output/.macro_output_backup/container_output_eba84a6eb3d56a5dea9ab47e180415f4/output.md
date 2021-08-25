`{bm-disable-all}`[ch1_code/src/FindLocations.py](ch1_code/src/FindLocations.py) (lines 11 to 32):`{bm-enable-all}`

```python
class Options(NamedTuple):
    hamming_distance: int = 0
    reverse_complement: bool = False


def find_kmer_locations(sequence: str, kmer: str, options: Options = Options()) -> List[int]:
    # Construct test kmers
    test_kmers = set()
    test_kmers.add(kmer)
    [test_kmers.add(alt_kmer) for alt_kmer in find_all_dna_kmers_within_hamming_distance(kmer, options.hamming_distance)]
    if options.reverse_complement:
        rc_kmer = reverse_complement(kmer)
        [test_kmers.add(alt_rc_kmer) for alt_rc_kmer in find_all_dna_kmers_within_hamming_distance(rc_kmer, options.hamming_distance)]

    # Slide over the sequence's kmers and check for matches against test kmers
    k = len(kmer)
    idxes = []
    for seq_kmer, i in slide_window(sequence, k):
        if seq_kmer in test_kmers:
            idxes.append(i)
    return idxes
```