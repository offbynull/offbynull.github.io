from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide
from Utils import HashableList, get_unique_amino_acid_masses_as_dict, contains_all_sorted

with open('/home/user/Downloads/dataset_240281_6(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

cyclic_peptide_experimental_spectrum = [int(w) for w in data.strip().split()]
cyclic_peptide_experimental_spectrum.sort()  # should be sorted already, but just in case
max_cyclic_peptide_experimental_spectrum = cyclic_peptide_experimental_spectrum[-1]

mass_table = get_unique_amino_acid_masses_as_dict()


candidate_peptides = {HashableList()}
final_peptides = set()
while len(candidate_peptides) > 0:
    # Branch
    new_candidate_peptides = set()
    for p in candidate_peptides:
        for m in mass_table:
            new_p = HashableList(p)
            new_p.append(m)
            new_candidate_peptides.add(new_p)
    candidate_peptides = new_candidate_peptides
    # Bound
    removal_set = set()
    for p in candidate_peptides:
        if sum(p) == max_cyclic_peptide_experimental_spectrum:
            if theoretical_spectrum_of_cyclic_peptide(p, mass_table) == cyclic_peptide_experimental_spectrum:
                final_peptides.add(p)
            removal_set.add(p)
        elif not contains_all_sorted(
                theoretical_spectrum_of_linear_peptide(p, mass_table),
                cyclic_peptide_experimental_spectrum):
            removal_set.add(p)
    candidate_peptides -= removal_set

ret = ' '.join(['-'.join([str(i) for i in p]) for p in final_peptides])
print(f'{ret}')