import typing
from collections import Counter
from typing import List


def group_fuzzy_convolution_matches(masses: List[float], tolerance: float) -> typing.Counter[float]:
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


def spectrum_convolution(experimental_spectrum: List[float], tolerance: float, min_mass=57.0, max_mass=200.0, round_digits=-1) -> typing.Counter[float]:
    min_mass -= tolerance
    max_mass += tolerance

    # it's expected that experimental_spectrum is sorted smallest to largest
    diffs = []
    for row_idx, row_mass in enumerate(experimental_spectrum):
        for col_idx, col_mass in enumerate(experimental_spectrum):
            mass_diff = row_mass - col_mass
            if round_digits != -1:
                mass_diff = round(mass_diff, round_digits)
            if min_mass <= mass_diff <= max_mass:
                diffs.append(mass_diff)

    return group_fuzzy_convolution_matches(diffs, tolerance)


if __name__ == '__main__':
    spectrum = [370.5, 374.4, 389.4, 391.2, 408.0, 419.2, 426.2, 442.3, 445.4, 460.3, 470.4, 476.4, 490.3, 504.3, 505.4, 518.2, 535.1, 545.5, 552.3, 561.3, 587.2, 599.3, 615.2, 616.4, 617.3, 632.4, 633.4, 635.2, 650.5, 651.4, 701.5, 702.4, 711.5, 717.3, 720.0, 729.3, 748.4, 761.6, 762.4, 763.4, 778.6, 779.4, 780.4, 781.4, 796.3, 861.4, 875.4, 876.4, 877.6, 878.4, 892.4, 893.4, 894.4, 895.5, 926.4, 943.4, 974.5, 975.5, 976.4, 978.4, 1004.5, 1006.5, 1021.5, 1022.7, 1023.5, 1038.5, 1039.3, 1041.5, 1042.4, 1056.5, 1118.6, 1119.6, 1136.6, 1137.6, 1138.5, 1155.5, 1156.6, 1167.6, 1170.6, 1184.4, 1219.6, 1221.5, 1222.6, 1238.6, 1239.6, 1249.5, 1255.5, 1265.5, 1266.5, 1267.6]

    differences = spectrum_convolution(spectrum[0:30], 0.6)
    differences = Counter([round(v, 0) for v in differences.elements()])
    print(f'{differences}')

    differences = spectrum_convolution(spectrum[30:60], 0.6)
    differences = Counter([round(v, 0) for v in differences.elements()])
    print(f'{differences}')

    differences = spectrum_convolution(spectrum[60:90], 0.6)
    differences = Counter([round(v, 0) for v in differences.elements()])
    print(f'{differences}')
