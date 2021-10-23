`{bm-disable-all}`[ch2_code/src/ScoreMotifUsingRelativeEntropy.py](ch2_code/src/ScoreMotifUsingRelativeEntropy.py) (lines 10 to 84):`{bm-enable-all}`

```python
# NOTE: This is different from the traditional version of entropy -- it doesn't negate the sum before returning it.
def calculate_entropy(probabilities_for_nuc: List[float]) -> float:
    ret = 0.0
    for value in probabilities_for_nuc:
        ret += value * (log(value, 2.0) if value > 0.0 else 0.0)
    return ret


def calculate_cross_entropy(probabilities_for_nuc: List[float], total_frequencies_for_nucs: List[float]) -> float:
    ret = 0.0
    for prob, total_freq in zip(probabilities_for_nuc, total_frequencies_for_nucs):
        ret += prob * (log(total_freq, 2.0) if total_freq > 0.0 else 0.0)
    return ret


def score_motif_relative_entropy(motif_matrix: List[str], source_strs: List[str]) -> float:
    # calculate frequency of nucleotide across all source strings
    nuc_counter = Counter()
    nuc_total = 0
    for source_str in source_strs:
        for nuc in source_str:
            nuc_counter[nuc] += 1
        nuc_total += len(source_str)
    nuc_freqs = dict([(k, v / nuc_total) for k, v in nuc_counter.items()])

    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    # count up each column
    counts = motif_matrix_count(motif_matrix)
    profile = motif_matrix_profile(counts)
    relative_entropy_per_col = []
    for c in range(cols):
        # get entropy of column in motif
        entropy = calculate_entropy(
            [
                profile['A'][c],
                profile['C'][c],
                profile['G'][c],
                profile['T'][c]
            ]
        )
        # get cross entropy of column in motif (mixes in global nucleotide frequencies)
        cross_entropy = calculate_cross_entropy(
            [
                profile['A'][c],
                profile['C'][c],
                profile['G'][c],
                profile['T'][c]
            ],
            [
                nuc_freqs['A'],
                nuc_freqs['C'],
                nuc_freqs['G'],
                nuc_freqs['T']
            ]
        )
        relative_entropy = entropy - cross_entropy
        # Right now relative_entropy is calculated by subtracting cross_entropy from (a negated) entropy. But, according
        # to the Pevzner book, the calculation of relative_entropy can be simplified to just...
        # def calculate_relative_entropy(probabilities_for_nuc: List[float], total_frequencies_for_nucs: List[float]) -> float:
        #     ret = 0.0
        #     for prob, total_freq in zip(probabilities_for_nuc, total_frequency_for_nucs):
        #         ret += value * (log(value / total_freq, 2.0) if value > 0.0 else 0.0)
        #     return ret
        relative_entropy_per_col.append(relative_entropy)

    # sum up entropies to get entropy of motif
    ret = sum(relative_entropy_per_col)

    # All of the other score_motif algorithms try to MINIMIZE score. In the case of relative entropy (this algorithm),
    # the greater the score is the better of a match it is. As such, negate this score so the existing algorithms can
    # still try to minimize.
    return -ret
```