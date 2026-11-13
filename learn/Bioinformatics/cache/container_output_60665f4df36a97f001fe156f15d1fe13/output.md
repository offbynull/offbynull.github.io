`{bm-disable-all}`[ch9_code/src/sequence_search/BLAST.py](ch9_code/src/sequence_search/BLAST.py) (lines 171 to 219):`{bm-enable-all}`

```python
def find_hsps(
        seq: str,
        k: int,
        db: dict[str, set[tuple[str, int]]],
        score_function: Callable[[str, str], float],
        score_min: float
):
    # Find high scoring segment pairs
    hsp_records = set()
    for kmer1, idx1_begin in slide_window(seq, k):
        # Find sequences for this kmer in the database
        found_seqs = db.get(kmer1, None)
        if found_seqs is None:
            continue
        # For each match, extend left-and-right until the alignment score begins to decrease
        for seq2, idx2_begin in found_seqs:
            last_idx1_begin, last_idx1_end = idx1_begin, idx1_begin + k
            last_idx2_begin, last_idx2_end = idx2_begin, idx2_begin + k
            last_kmer1 = seq[last_idx1_begin:last_idx1_end]
            last_kmer2 = seq2[last_idx2_begin:last_idx2_end]
            last_score = score_function(last_kmer1, last_kmer2)
            last_k = k
            while True:
                new_idx1_begin, new_idx1_end = last_idx1_begin, last_idx1_end
                new_idx2_begin, new_idx2_end = last_idx2_begin, last_idx2_end
                if new_idx1_begin > 0 and new_idx2_begin > 0:
                    new_idx1_begin -= 1
                    new_idx2_begin -= 1
                if new_idx1_begin < len(seq) - 1 and new_idx2_end < len(seq2) - 1:
                    new_idx1_end = new_idx1_end + 1
                    new_idx2_end = new_idx2_end + 1
                new_kmer1 = seq[new_idx1_begin:new_idx1_end]
                new_kmer2 = seq2[new_idx2_begin:new_idx2_end]
                new_score = score_function(new_kmer1, new_kmer2)
                # If current extension decreased the alignment score, stop. Add the PREVIOUS extension as a high-scoring
                # segment pair only if it scores high enough to be considered
                if new_score < last_score:
                    if last_score >= score_min:
                        record = last_score, last_k, (last_idx1_begin, seq), (last_idx2_begin, seq2)
                        hsp_records.add(record)
                    break
                last_score = new_score
                last_k = new_idx1_end - new_idx1_begin
                last_idx1_begin, last_idx1_end = new_idx1_begin, new_idx1_end
                last_idx2_begin, last_idx2_end = new_idx2_begin, new_idx2_end
                last_kmer1 = new_kmer1
                last_kmer2 = new_kmer2
    return hsp_records
```