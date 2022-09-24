```python
S = TypeVar('S', StringView, str)


def to_seeds(
        seq: S,
        mismatches: int
) -> list[S]:
    seed_cnt = mismatches + 1
    len_per_seed = ceil(len(seq) / seed_cnt)
    ret = []
    for i in range(0, len(seq), len_per_seed):
        capture_len = min(len(seq) - i, len_per_seed)
        ret.append(seq[i:i+capture_len])
    return ret


def seed_extension(
        test_sequence: S,
        found_seq_idx: int,
        found_seed_idx: int,
        seeds: list[S]
) -> tuple[int, int] | None:
    prefix_len = sum(len(seeds[i]) for i in range(0, found_seed_idx))
    start_idx = found_seq_idx - prefix_len
    if start_idx < 0:
        return None  # report out-of-bounds
    seq_idx = start_idx
    dist = 0
    for seed in seeds:
        block = test_sequence[seq_idx:seq_idx + len(seed)]
        if len(block) < len(seed):
            return None  # report out-of-bounds
        dist += hamming_distance(seed, block)
        seq_idx += len(seed)
    return start_idx, dist
```