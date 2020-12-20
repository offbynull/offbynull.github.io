import typing
from collections import Counter
from typing import List


# MARKDOWN
def group_masses_by_tolerance(masses: List[float], tolerance: float) -> typing.Counter[float]:
    masses = sorted(masses)
    length = len(masses)
    ret = Counter()
    for i, m1 in enumerate(masses):
        if m1 in ret:
            continue
        # search backwards
        left_limit = 0
        for j in range(i, -1, -1):
            m2 = masses[j]
            if abs(m2 - m1) > tolerance:
                break
            left_limit = j
        # search forwards
        right_limit = length - 1
        for j in range(i, length):
            m2 = masses[j]
            if abs(m2 - m1) > tolerance:
                break
            right_limit = j
        count = right_limit - left_limit + 1
        ret[m1] = count
    return ret


def spectrum_convolution(
        exp_spec: List[float],  # must be sorted smallest to largest
        tolerance: float,
        min_mass: float = 57.0,
        max_mass: float = 200.0,
        round_digits: int = -1,  # if set, rounds to this many digits past decimal point
        implied_zero: bool = False  # if set, run as if 0.0 were added to exp_spec
) -> typing.Counter[float]:
    min_mass -= tolerance
    max_mass += tolerance
    diffs = []
    for row_idx, row_mass in enumerate(exp_spec):
        for col_idx, col_mass in enumerate(exp_spec):
            mass_diff = row_mass - col_mass
            if round_digits != -1:
                mass_diff = round(mass_diff, round_digits)
            if min_mass <= mass_diff <= max_mass:
                diffs.append(mass_diff)
    if implied_zero:
        for mass in exp_spec:
            if min_mass <= mass <= max_mass:
                diffs.append(mass)
            if mass > max_mass:
                break
    return group_masses_by_tolerance(diffs, tolerance)
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec = [float(m) for m in input().strip().split()]
        exp_spec.sort()
        tolerance = float(input().strip())
        round_digits = int(input().strip())
        potential_aa_masses = spectrum_convolution(exp_spec, tolerance, round_digits=round_digits, implied_zero=True)
        print(f'The spectrum convolution for {exp_spec} is ...', end="\n\n")
        for aa_mass, count in potential_aa_masses.most_common():
            print(f' * {count}x{aa_mass}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()