from collections import Counter
from typing import List


# MARKDOWN
def spectrum_convolution(experimental_spectrum: List[float], min_mass=57.0, max_mass=200.0) -> List[float]:
    # it's expected that experimental_spectrum is sorted smallest to largest
    diffs = []
    for row_idx, row_mass in enumerate(experimental_spectrum):
        for col_idx, col_mass in enumerate(experimental_spectrum):
            mass_diff = row_mass - col_mass
            if min_mass <= mass_diff <= max_mass:
                diffs.append(mass_diff)
    diffs.sort()
    return diffs
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec = [float(m) for m in input().strip().split()]
        spectrum = spectrum_convolution(exp_spec)
        spectrum.sort()
        print(f'The spectrum convolution for {exp_spec} is ...', end="\n\n")
        for mass, count in Counter(spectrum).most_common():
            print(f' * {count}x{mass}', end="\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
