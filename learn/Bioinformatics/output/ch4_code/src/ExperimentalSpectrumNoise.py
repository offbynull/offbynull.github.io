from itertools import accumulate
from typing import List, TypeVar, Dict, Set


# MARKDOWN
def experimental_spectrum_noise(max_mass_charge_ratio_noise: float, charge_tendencies: Set[float]) -> float:
    return max_mass_charge_ratio_noise * abs(max(charge_tendencies))
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        max_mass_charge_ratio_noise = float(input().strip())
        charge_tendencies = {float(c) for c in input().strip().split()}
        exp_spec_noise = experimental_spectrum_noise(
            max_mass_charge_ratio_noise,
            charge_tendencies,
        )
        print(f'Given a max mass-to-charge ratio noise of ±{max_mass_charge_ratio_noise}'
              f' and charge tendencies {charge_tendencies},'
              f' the maximum noise per experimental spectrum mass is ±{exp_spec_noise}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()