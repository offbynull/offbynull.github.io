from statistics import mean


def estimate_coin_head_bias(
        flip_seqs: list[tuple[str, str]],
        flips_per_seq: int
):
    head_percentage_per_seq = []
    for _, seq in flip_seqs:
        perc = sum(1 for ch in seq if ch == 'H') / flips_per_seq
        head_percentage_per_seq.append(perc)
    a_percs = []
    b_percs = []
    for (coin, _), perc in zip(flip_seqs, head_percentage_per_seq):
        if coin == 'A':
            a_percs.append(perc)
        elif coin == 'B':
            b_percs.append(perc)
    return mean(a_percs), mean(b_percs)


if __name__ == '__main__':
    observed_flips = [
        ('A', 'HTTTHTTHTH'),
        ('B', 'HHHHTHHHHH'),
        ('B', 'HTHHHHHTHH'),
        ('A', 'HTTTTTHHTT'),
        ('B', 'THHHTHHHTH')
    ]
    print(f'{estimate_coin_head_bias(observed_flips, 10)=}')

    # THIS IS ESTIMATING THE COIN BIASES
    # IN:  header percentages + coin used per flip sequence (A or B)
    # OUT: estimated coin bias (A and B)
