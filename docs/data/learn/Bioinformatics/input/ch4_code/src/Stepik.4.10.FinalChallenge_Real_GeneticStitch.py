from itertools import product

from SelectAndMutate import SelectAndMutate
from NoisyScoreSpectrums import theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses, \
    score_spectrums, theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses
from NoisySpectrumConvolution import spectrum_convolution
from Utils import slide_window, get_unique_amino_acid_masses_as_dict

# This algorithm fails miserably. With some tweaking, it might work with the fake spectrum, but it doesn't converge to
# anything of value with the real specturm.

with open('real_spectrum.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
cyclopeptide_exp_spec = [float(w) for w in data.strip().split()]
cyclopeptide_exp_spec.sort()  # should be sorted already, but just in case

m = 15
noise_tolerance = 0.3  # max amount of noise per spectrum entry
guessed_len = 10  # how long you think the peptide is

cyclopeptide_exp_spec = [round(m - 1.007, 1) for m in cyclopeptide_exp_spec]  # remove mass for +1 charge and round

aa_mass_tolerance = noise_tolerance * 2
aa_masses = spectrum_convolution(cyclopeptide_exp_spec, aa_mass_tolerance, round_digits=0)
aa_mass_table = get_unique_amino_acid_masses_as_dict()

ga_cycles_per_iteration = 10
last_n_scores = 10
subpeptides_pop_size = 100000
subpeptide_len = 6
subpeptides_next = None
final_peptide_len = 10
max_nonoverlapping = 1

head_map = dict()
tail_map = dict()
while subpeptide_len <= final_peptide_len:
    print(f'Expanding from len={subpeptide_len}')

    ga = SelectAndMutate(
        cyclopeptide_exp_spec,
        aa_mass_table,
        aa_mass_tolerance,
        peptide_len=subpeptide_len,
        population_size=subpeptides_pop_size,
        population_initial=subpeptides_next,
        parent_score_fitness_threshold=0
    )

    for _ in range(ga_cycles_per_iteration):
        ga.select_and_mutate()

    subpeptides = ga.dump()
    scores = [0] * len(subpeptides)
    for i, subpeptide in enumerate(subpeptides):
        theo_spec = theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses(
            subpeptide,
            aa_mass_table,
            aa_mass_tolerance
        )
        score = score_spectrums(cyclopeptide_exp_spec, theo_spec)
        score_within = score[0]
        scores[i] = score_within
    scores_unique = sorted(list(set(scores)), reverse=True)
    scores_threshold = scores[min(len(scores), last_n_scores)]
    subpeptides = list(
        map(
            lambda y: y[0],
            filter(
                lambda x: x[1] >= scores_threshold,
                zip(subpeptides, scores)
            )
        )
    )

    overlap_len = subpeptide_len - max_nonoverlapping
    for head_sp in subpeptides:
        head = tuple(head_sp[:overlap_len])
        head_map.setdefault(head, []).append(head_sp)
        tail = tuple(head_sp[-overlap_len:])
        tail_map.setdefault(tail, []).append(head_sp)

    subpeptide_next_len = subpeptide_len + 1
    subpeptides_next = []
    for head_sp in subpeptides:
        tail = tuple(head_sp[-overlap_len:])
        neighbours = head_map.get(tail)
        if neighbours is None:
            continue
        for tail_sp in neighbours:
            sp = head_sp[:-overlap_len] + tail_sp
            for sp_window, _ in slide_window(sp, subpeptide_next_len):
                subpeptides_next.append(sp_window)

    for p in subpeptides_next:
        p_theo_spec = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, aa_mass_tolerance)
        score = score_spectrums(cyclopeptide_exp_spec, p_theo_spec)
        print(f'{p} len={len(p)} score={score}')

    subpeptide_len = subpeptide_next_len
