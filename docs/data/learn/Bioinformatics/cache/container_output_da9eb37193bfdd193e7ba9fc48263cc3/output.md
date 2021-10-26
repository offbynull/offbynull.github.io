`{bm-disable-all}`[ch6_code/src/synteny_graph/MatchMerger.py](ch6_code/src/synteny_graph/MatchMerger.py) (lines 18 to 65):`{bm-enable-all}`

```python
def distance_merge(matches: Iterable[Match], radius: int, angle_half_maw: int = 45) -> List[Match]:
    min_x = min(m.x_axis_chromosome_min_idx for m in matches)
    max_x = max(m.x_axis_chromosome_max_idx for m in matches)
    min_y = min(m.y_axis_chromosome_min_idx for m in matches)
    max_y = max(m.y_axis_chromosome_max_idx for m in matches)
    indexer = MatchSpatialIndexer(min_x, max_x, min_y, max_y)
    for m in matches:
        indexer.index(m)
    ret = []
    remaining = set(matches)
    while remaining:
        m = next(iter(remaining))
        found = indexer.scan(m, radius, angle_half_maw)
        merged = Match.merge(found)
        for _m in found:
            indexer.unindex(_m)
            remaining.remove(_m)
        ret.append(merged)
    return ret


def overlap_filter(
        matches: Iterable[Match],
        max_filter_length: float,
        max_merge_distance: float
) -> List[Match]:
    clipper = MatchOverlapClipper(max_filter_length, max_merge_distance)
    for m in matches:
        while True:
            # When you attempt to add a match to the clipper, the clipper may instead ask you to make a set of changes
            # before it'll accept it. Specifically, the clipper may ask you to replace a bunch of existing matches that
            # it's already indexed and then give you a MODIFIED version of m that it'll accept once you've applied
            # those replacements
            changes_requested = clipper.index(m)
            if not changes_requested:
                break
            # replace existing entries in clipper
            for from_m, to_m in changes_requested.existing_matches_to_replace.items():
                clipper.unindex(from_m)
                if to_m:
                    res = clipper.index(to_m)
                    assert res is None
            # replace m with a revised version -- if None it means m isn't needed (its been filtered out)
            m = changes_requested.revised_match
            if not m:
                break
    return list(clipper.get())
```