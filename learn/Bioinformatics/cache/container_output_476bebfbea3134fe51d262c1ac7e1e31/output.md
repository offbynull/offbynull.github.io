`{bm-disable-all}`[ch9_code/src/sequence_search/BLAST.py](ch9_code/src/sequence_search/BLAST.py) (lines 140 to 166):`{bm-enable-all}`

```python
def find_similar_kmers(
        kmer: str,
        alphabet: str,
        score_function: Callable[[str, str], float],
        score_min: float
) -> Generator[str, None, None]:
    k = len(kmer)
    for neighbouring_kmer in product(alphabet, repeat=k):
        neighbouring_kmer = ''.join(neighbouring_kmer)
        alignment_score = score_function(kmer, neighbouring_kmer)
        if alignment_score >= score_min:
            yield neighbouring_kmer


def create_database(
        seqs: set[str],
        k: int,
        alphabet: str,
        alignment_score_function: Callable[[str, str], float],
        alignment_min: float
) -> dict[str, set[tuple[str, int]]]:
    db = defaultdict(set)
    for seq in seqs:
        for kmer, idx in slide_window(seq, k):
            for neighbouring_kmer in find_similar_kmers(kmer, alphabet, alignment_score_function, alignment_min):
                db[neighbouring_kmer].add((seq, idx))
    return db
```