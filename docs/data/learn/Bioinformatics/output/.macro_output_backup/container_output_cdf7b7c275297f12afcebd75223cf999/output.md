`{bm-disable-all}`[ch4_code/src/SpectrumScore.py](ch4_code/src/SpectrumScore.py) (lines 10 to 129):`{bm-enable-all}`

```python
def scan_left(
        exp_spec: List[float],
        exp_spec_lo_idx: int,
        exp_spec_start_idx: int,
        theo_mid_mass: float,
        theo_min_mass: float
) -> Optional[int]:
    found_dist = None
    found_idx = None
    for idx in range(exp_spec_start_idx, exp_spec_lo_idx - 1, -1):
        exp_mass = exp_spec[idx]
        if exp_mass < theo_min_mass:
            break
        dist_to_theo_mid_mass = abs(exp_mass - theo_mid_mass)
        if found_dist is None or dist_to_theo_mid_mass < found_dist:
            found_idx = idx
            found_dist = dist_to_theo_mid_mass
    return found_idx


def scan_right(
        exp_spec: List[float],
        exp_spec_hi_idx: int,
        exp_spec_start_idx: int,
        theo_mid_mass: float,
        theo_max_mass: float
) -> Optional[int]:
    found_dist = None
    found_idx = None
    for idx in range(exp_spec_start_idx, exp_spec_hi_idx):
        exp_mass = exp_spec[idx]
        if exp_mass > theo_max_mass:
            break
        dist_to_theo_mid_mass = abs(exp_mass - theo_mid_mass)
        if found_dist is None or dist_to_theo_mid_mass < found_dist:
            found_idx = idx
            found_dist = dist_to_theo_mid_mass
    return found_idx


def find_closest_within_tolerance(
        exp_spec: List[float],
        exp_spec_lo_idx: int,
        exp_spec_hi_idx: int,
        theo_exact_mass: float,
        theo_min_mass: float,
        theo_max_mass: float
) -> Optional[int]:
    # Binary search exp_spec for the where theo_mid_mass would be inserted (left-most index chosen if already there).
    start_idx = bisect_left(exp_spec, theo_exact_mass, lo=exp_spec_lo_idx, hi=exp_spec_hi_idx)
    if start_idx == exp_spec_hi_idx:
        start_idx -= 1
    # From start_idx - 1, walk left to find the closest possible value to theo_mid_mass
    left_idx = scan_left(exp_spec, exp_spec_lo_idx, start_idx - 1, theo_exact_mass, theo_min_mass)
    # From start_idx, walk right to find the closest possible value to theo_mid_mass
    right_idx = scan_right(exp_spec, exp_spec_hi_idx, start_idx, theo_exact_mass, theo_max_mass)
    if left_idx is None and right_idx is None:  # If nothing found, return None
        return None
    if left_idx is None:  # If found something while walking left but not while walking right, return left
        return right_idx
    if right_idx is None:  # If found something while walking right but not while walking left, return right
        return left_idx
    # Otherwise, compare left and right to see which is close to theo_mid_mass and return that
    left_exp_mass = exp_spec[left_idx]
    left_dist_to_theo_mid_mass = abs(left_exp_mass - theo_exact_mass)
    right_exp_mass = exp_spec[left_idx]
    right_dist_to_theo_mid_mass = abs(right_exp_mass - theo_exact_mass)
    if left_dist_to_theo_mid_mass < right_dist_to_theo_mid_mass:
        return left_idx
    else:
        return right_idx


def score_spectrums(
        exp_spec: List[float],  # must be sorted asc
        theo_spec_with_tolerances: List[Tuple[float, float, float]]  # must be sorted asc, items are (expected,min,max)
) -> Tuple[int, float, float]:
    dist_score = 0.0
    within_score = 0
    exp_spec_lo_idx = 0
    exp_spec_hi_idx = len(exp_spec)
    for theo_mass in theo_spec_with_tolerances:
        # Find closest exp_spec mass for theo_mass
        theo_exact_mass, theo_min_mass, theo_max_mass = theo_mass
        exp_idx = find_closest_within_tolerance(
            exp_spec,
            exp_spec_lo_idx,
            exp_spec_hi_idx,
            theo_exact_mass,
            theo_min_mass,
            theo_max_mass
        )
        if exp_idx is None:
            continue
        # Calculate how far the found mass is from the ideal mass (theo_exact_mass) -- a perfect match will add 1.0 to
        # score, the farther out it is away the less gets added to score (min added will be 0.5).
        exp_mass = exp_spec[exp_idx]
        dist = abs(exp_mass - theo_exact_mass)
        max_dist = theo_max_mass - theo_min_mass
        if max_dist > 0.0:
            closeness = 1.0 - (dist / max_dist)
        else:
            closeness = 1.0
        dist_score += closeness
        # Increment within_score for each match. The above block increases dist_score as the found mass gets closer to
        # theo_exact_mass. There may be a case where a peptide with 6 of 10 AAs matches exactly (6 * 1.0) while another
        # peptide with 10 of 10 AAs matching very loosely (10 * 0.5) -- the first peptide will incorrectly win out if
        # only dist_score were used.
        within_score += 1
        # Move up the lower bound for what to consider in exp_spec such that it it's after the exp_spec mass found
        # in this cycle. That is, the next cycle won't consider anything lower than the mass that was found here. This
        # is done because theo_spec may contain multiple copies of the same mass, but a real experimental spectrum won't
        # do that (e.g. a peptide containing 57 twice will have two entries for 57 in its theoretical spectrum, but a
        # real experimental spectrum for that same peptide will only contain 57 -- anything with mass of 57 will be
        # collected into the same bin).
        exp_spec_lo_idx = exp_idx + 1
        if exp_spec_lo_idx == exp_spec_hi_idx:
            break
    return within_score, dist_score, 0.0 if within_score == 0 else dist_score / within_score
```