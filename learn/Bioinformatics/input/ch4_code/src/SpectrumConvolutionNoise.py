from typing import Set

from ExperimentalSpectrumNoise import experimental_spectrum_noise


# MARKDOWN
def spectrum_convolution_noise(exp_spec_mass_noise: float) -> float:
    return 2.0 * exp_spec_mass_noise
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec_mass_noise = float(input().strip())
        aa_noise = spectrum_convolution_noise(
            exp_spec_mass_noise,
        )
        print(f'Given a max experimental spectrum mass noise of ±{exp_spec_mass_noise},'
              f' the maximum noise per amino acid derived from an experimental spectrum is ±{aa_noise}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()