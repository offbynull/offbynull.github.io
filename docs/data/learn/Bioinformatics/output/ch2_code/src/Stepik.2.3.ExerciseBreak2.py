from ScoreMotifUsingEntropy import score_motify_entropy

if __name__ == '__main__':
    entropy = score_motify_entropy([
        'TCGGGGgTTTtt'.upper(),
        'cCGGtGAcTTaC'.upper(),
        'aCGGGGATTTtC'.upper(),
        'TtGGGGAcTTtt'.upper(),
        'aaGGGGAcTTCC'.upper(),
        'TtGGGGAcTTCC'.upper(),
        'TCGGGGATTcat'.upper(),
        'TCGGGGATTcCt'.upper(),
        'TaGGGGAacTaC'.upper(),
        'TCGGGtATaaCC'.upper()
    ])

    print(f'{entropy}')