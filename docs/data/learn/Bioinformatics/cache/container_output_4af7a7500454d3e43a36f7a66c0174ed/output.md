`{bm-disable-all}`[ch10_code/src/profile_hmm/ProfileToHMMProbabilities.py](ch10_code/src/profile_hmm/ProfileToHMMProbabilities.py) (lines 10 to 37):`{bm-enable-all}`

```python
from profile_hmm.HMMSingleElementAlignment_EmitDelete import ELEM


def walk_row_of_profile(profile: Profile[ELEM], row: int):
    path = []
    stable_col_cnt = profile.col_count
    r = -1
    c = -1
    for stable_col_idx in range(stable_col_cnt):
        # is anything inserted before the stable column? if yes, indicate an insertion
        if profile.insertion_before(stable_col_idx).is_set(row):
            elems = profile.insertion_before(stable_col_idx).values[row]
            path.append(((r, c), (r, c+1), 'I', elems[:]))  # didn't move to next column (stays at c-1)
            c += 1
        # id anything at the stable column? if yes, indicate a match / no, indicate a deletion
        if profile.match(stable_col_idx).is_set(row):
            elem = profile.match(stable_col_idx).values[row]
            path.append(((r, c), (r+1, c+1), 'M', [elem]))  # did move to next column via a match (from c-1 to c)
            r += 1
            c += 1
        else:
            path.append(((r, c), (r+1, c), 'D', []))  # did move to next column via a delete (from c-1 to c)
            r += 1
    if profile.insertion_after(stable_col_cnt-1).is_set(row):
        elems = profile.insertion_after(stable_col_cnt-1).values[row]
        path.append(((r, c), (r, c+1), 'I', elems[:]))
        c += 1
    return path
```