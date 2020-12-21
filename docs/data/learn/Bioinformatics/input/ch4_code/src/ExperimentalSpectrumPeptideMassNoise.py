from SpectrumConvolutionNoise import spectrum_convolution_noise


# For an exp spec...
#
# If the mass was captured and found, it'll have noise. Assume an experimental spectrum with ±1Da noise. If the peptide
# mass exists in this experimental spectrum, it'll have ±1Da noise it. For example, the peptide 57-57 has an exact mass
# of 114Da, but if that mass gets placed into the experimental spectrum it may show up as anywhere between 113Da to
# 115Da.
#
# Given that same experimental spectrum, running a spectrum convolution to derive the amino acid masses ends up giving
# back amino acid masses with ±2Da noise. For example, the mass 57Da may be derived as anywhere between 55Da to 59Da.
# Assuming that you're building a test peptide with the low end (55Da), 55Da + 55Da = 110Da. Compared against the high
# end of the experimental spectrum's peptide mass (115Da), it's 5Da away.


# MARKDOWN
def experimental_spectrum_peptide_mass_noise(exp_spec_mass_noise: float, peptide_len: int) -> float:
    aa_mass_noise = spectrum_convolution_noise(exp_spec_mass_noise)
    return aa_mass_noise * peptide_len + exp_spec_mass_noise
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec_mass_noise = float(input().strip())
        peptide_len = int(input().strip())
        peptide_mass_noise = experimental_spectrum_peptide_mass_noise(
            exp_spec_mass_noise,
            peptide_len
        )
        print(f'Given an experimental spectrum mass noise of ±{exp_spec_mass_noise}'
              f' and expected peptide length of {peptide_len},'
              f' the maximum noise for an experimental spectrum\'s peptide mass is ±{peptide_mass_noise}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()