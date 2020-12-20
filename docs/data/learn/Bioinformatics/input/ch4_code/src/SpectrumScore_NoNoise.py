from typing import List


# Count the number of intersections (an item must be in BOTH lists to be included). For example...
# [0, 99, 113, 128] vs [0, 128, 227] has a score of 2 (intersection is [0, 128])
#
# It's assumed that both spectra are sorted smallest to largest.
# MARKDOWN
def score_spectrums(
        s1: List[float],  # must be sorted ascending
        s2: List[float]   # must be sorted ascending
) -> int:
    idx_s1 = 0
    idx_s2 = 0
    score = 0
    while idx_s1 < len(s1) and idx_s2 < len(s2):
        s1_mass = s1[idx_s1]
        s2_mass = s2[idx_s2]
        if s1_mass < s2_mass:
            idx_s1 += 1
        elif s1_mass > s2_mass:
            idx_s2 += 1
        else:
            idx_s1 += 1
            idx_s2 += 1
            score += 1
    return score
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec = [float(m) for m in input().strip().split()]
        exp_spec.sort()
        theo_spec = [float(m) for m in input().strip().split()]
        theo_spec.sort()
        score = score_spectrums(exp_spec, theo_spec)
        print(f'The spectrum score for...', end="\n\n")
        print(f'{exp_spec}', end="\n\n")
        print(f'... vs ...', end="\n\n")
        print(f'{theo_spec}', end="\n\n")
        print(f'... is {score}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()