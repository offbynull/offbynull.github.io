from math import log
from typing import List, Dict


def calculate_entropy(values: List[float]) -> float:
    ret = 0.0
    for value in values:
        ret += value * (log(value, 2.0) if value > 0.0 else 0.0)
    ret = -ret
    return ret


# For each column in a motif matrix, count up how many times each nucleotide appears.
def column_count_by_element(alignment_matrix: List[str], elements: str) -> Dict[str, List[int]]:
    rows = len(alignment_matrix)
    cols = len(alignment_matrix[0])

    ret = {}
    for ch in elements:
        ret[ch] = [0] * cols

    for c in range(0, cols):
        for r in range(0, rows):
            item = alignment_matrix[r][c]
            ret[item][c] += 1

    return ret


# For each column in a motif matrix, count up how many times each nucleotide appears.
def column_profile_by_element(alignmnet_matrix_counts: Dict[str, List[int]]) -> Dict[str, List[float]]:
    ret = {}
    for elem, counts in alignmnet_matrix_counts.items():
        ret[elem] = [0.0] * len(counts)

    cols = len(counts)  # all elems should have the same len, so just grab the last one that was walked over
    for i in range(cols):
        total = 0
        for elem in alignmnet_matrix_counts.keys():
            total += alignmnet_matrix_counts[elem][i]
        for elem in alignmnet_matrix_counts.keys():
            ret[elem][i] = alignmnet_matrix_counts[elem][i] / total

    return ret


def score_alignment_entropy(alignment_matrix: List[str], elements: str) -> float:
    rows = len(alignment_matrix)
    cols = len(alignment_matrix[0])

    # count up each column
    counts = column_count_by_element(alignment_matrix, elements)
    profile = column_profile_by_element(counts)

    # prob dist to entropy
    entropy_per_col = []
    for c in range(cols):
        freqs = [profile[e][c] for e in elements]
        entropy = calculate_entropy(freqs)
        entropy_per_col.append(entropy)

    # sum up column entropies to get entropy of alignment  -- this is the score of the alignment
    total_entropy = sum(entropy_per_col)

    # the more conserved a column is the lower its score will be... since our sequence alignment algorithms are looking
    # for the maximum score, negate the total entropy so that'll be flipped around: the more conserved, the higher the
    # score.
    return -total_entropy


elements = 'ACDEFGHIKLMNPQRSTVWY-'  # amino acid elements, gap added for indels

m1 = [
    'YAFDLGYTCMFPVLLGGGELHIVQKETYTAPDEIAHYIKEHGITYIKLTPSLFHTIVNTA',
    '-AFDVSAGDFARALLTGGQLIVCPNEVKMDPASLYAIIKKYDITIFEATPALVIPLMEYI',
    'IAFDASSWEIYAPLLNGGTVVCIDYYTTIDIKALEAVFKQHHIRGAMLPPALLKQCLVSA'
]
score1 = score_alignment_entropy(m1, elements)
print(f'{score1}')

m2 = [
    'SFAFDANFESLRLIVLGGEKIIPIDVIAFRKMYGHTE-FINHYGPTEATIGA',
    '-YEQKLDISQLQILIVGSDSCSMEDFKTLVSRFGSTIRIVNSYGVTEACIDS',
    '----PTMISSLEILFAAGDRLSSQDAILARRAVGSGV-Y-NAYGPTENTVLS'
]
score2 = score_alignment_entropy(m2, elements)
print(f'{score2}')