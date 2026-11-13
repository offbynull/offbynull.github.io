`{bm-disable-all}`[ch5_code/src/global_alignment/GlobalMultipleAlignment_Greedy.py](ch5_code/src/global_alignment/GlobalMultipleAlignment_Greedy.py) (lines 17 to 84):`{bm-enable-all}`

```python
class ProfileWeightLookup(WeightLookup):
    def __init__(self, total_seqs: int, backing_2d_lookup: WeightLookup):
        self.total_seqs = total_seqs
        self.backing_wl = backing_2d_lookup

    def lookup(self, *elements: Tuple[ELEM_OR_COLUMN, ...]):
        col: Tuple[ELEM, ...] = elements[0]
        elem: ELEM = elements[1]

        if col is None:
            return self.backing_wl.lookup(elem, None)  # should map to indel score
        elif elem is None:
            return self.backing_wl.lookup(None, col[0])  # should map to indel score
        else:
            probs = {elem: count / self.total_seqs for elem, count in Counter(e for e in col if e is not None).items()}
            ret = 0.0
            for p_elem, prob in probs.items():
                val = self.backing_wl.lookup(elem, p_elem) * prob
                ret = max(val, ret)
            return ret


def global_alignment(
        seqs: List[List[ELEM]],
        weight_lookup_2way: WeightLookup,
        weight_lookup_multi: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ...]]]:
    seqs = seqs[:]  # copy
    # Get initial best 2-way alignment
    highest_res = None
    highest_seqs = None
    for s1, s2 in combinations(seqs, r=2):
        if s1 is s2:
            continue
        res = GlobalAlignment_Matrix.global_alignment(s1, s2, weight_lookup_2way)
        if highest_res is None or res[0] > highest_res[0]:
            highest_res = res
            highest_seqs = s1, s2
    seqs.remove(highest_seqs[0])
    seqs.remove(highest_seqs[1])
    total_seqs = 2
    final_alignment = highest_res[1]
    # Build out profile matrix from alignment and continually add to it using 2-way alignment
    if seqs:
        s1 = highest_res[1]
        while seqs:
            profile_weight_lookup = ProfileWeightLookup(total_seqs, weight_lookup_2way)
            _, alignment = max(
                [GlobalAlignment_Matrix.global_alignment(s1, s2, profile_weight_lookup) for s2 in seqs],
                key=lambda x: x[0]
            )
            # pull out s1 from alignment and flatten for next cycle
            s1 = []
            for e in alignment:
                if e[0] is None:
                    s1 += [((None, ) * total_seqs) + (e[1], )]
                else:
                    s1 += [(*e[0], e[1])]
            # pull out s2 from alignment and remove from seqs
            s2 = [e for _, e in alignment if e is not None]
            seqs.remove(s2)
            # increase seq count
            total_seqs += 1
        final_alignment = s1
    # Recalculate score based on multi weight lookup
    final_weight = sum(weight_lookup_multi.lookup(*elems) for elems in final_alignment)
    return final_weight, final_alignment
```