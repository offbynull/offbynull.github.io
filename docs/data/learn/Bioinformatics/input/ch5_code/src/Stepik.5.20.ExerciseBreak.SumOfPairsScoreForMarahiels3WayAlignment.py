import itertools
from typing import List

# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.


def backing_score_func(e1:str, e2:str):
    if e1 == e2:
        return 1
    else:
        return 0


def score_alignment_sum_of_pairs(alignment_matrix: List[str]) -> float:
    rows = len(alignment_matrix)
    cols = len(alignment_matrix[0])

    pair_it = itertools.permutations(range(rows), r=2)  # get all pais of seqs
    pairs = {frozenset(c) for c in pair_it}  # remove dupes -- e.g. treat seqs (0,1) as equiv of seqs (1,0)

    # count up each column
    total_score = 0
    for c in range(cols):
        col_score = 0
        for r1, r2 in pairs:
            pair_score = backing_score_func(alignment_matrix[r1][c], alignment_matrix[r2][c])
            col_score += pair_score
        total_score += col_score

    return total_score


m1 = [
    'YAFDLGYTCMFPVLLGGGELHIVQKETYTAPDEIAHYIKEHGITYIKLTPSLFHTIVNTA',
    '-AFDVSAGDFARALLTGGQLIVCPNEVKMDPASLYAIIKKYDITIFEATPALVIPLMEYI',
    'IAFDASSWEIYAPLLNGGTVVCIDYYTTIDIKALEAVFKQHHIRGAMLPPALLKQCLVSA'
]
score1 = score_alignment_sum_of_pairs(m1)
print(f'{score1}')

m2 = [
    'SFAFDANFESLRLIVLGGEKIIPIDVIAFRKMYGHTE-FINHYGPTEATIGA',
    '-YEQKLDISQLQILIVGSDSCSMEDFKTLVSRFGSTIRIVNSYGVTEACIDS',
    '----PTMISSLEILFAAGDRLSSQDAILARRAVGSGV-Y-NAYGPTENTVLS'
]
score2 = score_alignment_sum_of_pairs(m2)
print(f'{score2}')