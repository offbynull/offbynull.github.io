from itertools import accumulate
from typing import List, TypeVar, Dict, Set


# MARKDOWN
def experimental_spectrum(mass_charge_ratios: List[float], charge_tendencies: Set[float]) -> List[float]:
    ret = [0.0]  # implied -- subpeptide of length 0
    for mcr in mass_charge_ratios:
        for charge in charge_tendencies:
            ret.append(mcr * charge)
    ret.sort()
    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        mass_charge_ratios = [float(r) for r in input().strip().split()]
        charge_tendencies = {float(c) for c in input().strip().split()}
        spectrum = experimental_spectrum(
            mass_charge_ratios,
            charge_tendencies,
        )
        print(f'The experimental spectrum for the mass-to-charge ratios...\n\n{mass_charge_ratios}\n\n... and charge tendencies...\n\n{charge_tendencies}\n\n... is...\n\n{spectrum}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()