`{bm-disable-all}`[ch6_code/src/synteny_graph/Match.py](ch6_code/src/synteny_graph/Match.py) (lines 176 to 232):`{bm-enable-all}`

```python
@staticmethod
def create_from_genomes(
        k: int,
        cyclic: bool,  # True if chromosomes are cyclic
        genome1: Dict[str, str],  # chromosome id -> dna string
        genome2: Dict[str, str]   # chromosome id -> dna string
) -> List[Match]:
    # lookup tables for data1
    fwd_kmers1 = defaultdict(list)
    rev_kmers1 = defaultdict(list)
    for chr_name, chr_data in genome1.items():
        for kmer, idx in slide_window(chr_data, k, cyclic):
            fwd_kmers1[kmer].append((chr_name, idx))
            rev_kmers1[dna_reverse_complement(kmer)].append((chr_name, idx))
    # lookup tables for data2
    fwd_kmers2 = defaultdict(list)
    rev_kmers2 = defaultdict(list)
    for chr_name, chr_data in genome2.items():
        for kmer, idx in slide_window(chr_data, k, cyclic):
            fwd_kmers2[kmer].append((chr_name, idx))
            rev_kmers2[dna_reverse_complement(kmer)].append((chr_name, idx))
    # match
    matches = []
    fwd_key_matches = set(fwd_kmers1.keys())
    fwd_key_matches.intersection_update(fwd_kmers2.keys())
    for kmer in fwd_key_matches:
        idxes1 = fwd_kmers1.get(kmer, [])
        idxes2 = fwd_kmers2.get(kmer, [])
        for (chr_name1, idx1), (chr_name2, idx2) in product(idxes1, idxes2):
            m = Match(
                y_axis_chromosome=chr_name1,
                y_axis_chromosome_min_idx=idx1,
                y_axis_chromosome_max_idx=idx1 + k - 1,
                x_axis_chromosome=chr_name2,
                x_axis_chromosome_min_idx=idx2,
                x_axis_chromosome_max_idx=idx2 + k - 1,
                type=MatchType.NORMAL
            )
            matches.append(m)
    rev_key_matches = set(fwd_kmers1.keys())
    rev_key_matches.intersection_update(rev_kmers2.keys())
    for kmer in rev_key_matches:
        idxes1 = fwd_kmers1.get(kmer, [])
        idxes2 = rev_kmers2.get(kmer, [])
        for (chr_name1, idx1), (chr_name2, idx2) in product(idxes1, idxes2):
            m = Match(
                y_axis_chromosome=chr_name1,
                y_axis_chromosome_min_idx=idx1,
                y_axis_chromosome_max_idx=idx1 + k - 1,
                x_axis_chromosome=chr_name2,
                x_axis_chromosome_min_idx=idx2,
                x_axis_chromosome_max_idx=idx2 + k - 1,
                type=MatchType.REVERSE_COMPLEMENT
            )
            matches.append(m)
    return matches
```