import typing
from collections import Counter
from itertools import accumulate
from typing import List, Set

# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# THIS IS EXACTLY THE SAME AS Stepik.4.7.CodeChallenge.LeaderboardCyclopeptideSequencing.py EXCEPT THAT THE INPUT IS FOR SUPER NOISY DATA (25% NOISE)
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER
# AND THAT IT RETURNS A SET OF LEADERS, NOT JUST 1 LEADER

with open('/home/user/Downloads/dataset_240282_10.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.split('\n')
n = int(data[0].strip())
spectrum = Counter([int(w) for w in data[1].strip().split()])
weights_table = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]


def is_consistent_with_spectrum(linear_peptide_theoretical_spectrum: typing.Counter[int]) -> bool:
    for k, v in linear_peptide_theoretical_spectrum.items():
        if spectrum[k] < v:
            return False
    return True


def cyclopeptide_spectrum(peptide: List[int]) -> typing.Counter[int]:
    prefix_masses = [0]
    for i, w in enumerate(peptide):
        prev_mass = prefix_masses[i]
        next_mass = prev_mass + w
        prefix_masses.append(next_mass)
    ret = [0]
    for k_end in range(0, len(prefix_masses)):
        for k_start in range(0, k_end):
            min_mass = prefix_masses[k_start]
            max_mass = prefix_masses[k_end]
            ret.append(max_mass - min_mass)
            if k_start > 0 and k_end < len(peptide):
                ret.append(prefix_masses[-1] - (prefix_masses[k_end] - prefix_masses[k_start]))
    return Counter(ret)


def linear_peptid_spectrum(peptide: List[int]) -> typing.Counter[int]:
    ret = Counter([0])
    for i in range(len(peptide)):
        ret += Counter(list(accumulate([w for w in peptide[i:]])))
    return ret


def linear_score(peptide_spectrum: typing.Counter[int], expected_spectrum: typing.Counter[int]) -> int:
    keys = peptide_spectrum.keys() | expected_spectrum.keys()
    return sum([min(peptide_spectrum[k], expected_spectrum[k]) for k in keys])


def trim_leaderboard(leaderboard: List[List[int]], expected_spectrum: typing.Counter[int], n: int) -> List[List[int]]:
    if len(leaderboard) == 0:
        return leaderboard
    scores = [linear_score(linear_peptid_spectrum(p), expected_spectrum) for p in leaderboard]
    sorted_peptides_and_scores = list(sorted(zip(leaderboard, scores), key=lambda x: x[1], reverse=True))
    for j in range(n + 1, len(sorted_peptides_and_scores)):
        if sorted_peptides_and_scores[n][1] > sorted_peptides_and_scores[j][1]:
            return [p for p, _ in sorted_peptides_and_scores[:j-1]]
    return [p for p, _ in sorted_peptides_and_scores]


leaderboard = [[]]
leader_peptides = [next(iter(leaderboard))]

while len(leaderboard) > 0:
    # Branch
    new_leaderboard = []
    for p in leaderboard:
        for w in weights_table:
            new_p = p[:]
            new_p.append(w)
            new_leaderboard.append(new_p)
    leaderboard = new_leaderboard
    # Bound
    new_leaderboard = []
    for p in leaderboard:
        if sum(p) > max(spectrum.elements()):
            continue
        elif sum(p) == max(spectrum.elements()):
            if linear_score(Counter(p), spectrum) > linear_score(Counter(leader_peptides[0]), spectrum):
                leader_peptides = [p]
            elif linear_score(Counter(p), spectrum) == linear_score(Counter(leader_peptides[0]), spectrum):
                leader_peptides.append(p)
        new_leaderboard.append(p)
    leaderboard = new_leaderboard
    leaderboard = trim_leaderboard(leaderboard, spectrum, n)

FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
FIX ME: FIND THE ONES THAT ARE CYCLES OF EACH OTHER AND DE-DUPE BECAUSE WE ARE SEARCHING FOR CYCLIC PEPTIDES
cp_spectrums = [cyclopeptide_spectrum(p)for p in leader_peptides]

ret = ' '.join(['-'.join([str(i) for i in p]) for p in leader_peptides])
print(f'{ret}')