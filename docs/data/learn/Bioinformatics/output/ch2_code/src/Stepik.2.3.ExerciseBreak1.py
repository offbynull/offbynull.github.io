# Originally I thought the answer was 150. It was wrong.
#
# Then I saw the solution...
#     In a motif matrix, the (potential) motif is determined by the nucleotides which have the maximum count in a
#     column. We have 10 nucleotides in a column, and there are four nucleotide types n₀, n₁, n₂, n₃. We are looking for
#     the min(#n₀) where #n₀ + #n₁ + #n₂ + #n₃ = 10 and #n₀ > #n₁ + #n₂ + #n₃. #n₀ must be ⌈10/4⌉ = 3. Then the score
#     for each column will be 7 and score(motif) = 7*15 = 105.
#
# Which makes absolutely no sense and seems to be introducing a new requirement for a column that was never discussed
# prior to the answer being show. I tried to replicate the answer as code but wasn't able to reach the same result.

combos = []
for n0_cnt in range(10 + 1):  # 0 to 10 inclusive
    for n1_cnt in range(10 + 1):  # 0 to 10 inclusive
        for n2_cnt in range(10 + 1):  # 0 to 10 inclusive
            for n3_cnt in range(10 + 1):  # 0 to 10 inclusive
                if n0_cnt + n1_cnt + n2_cnt + n3_cnt == 10 and n0_cnt > n1_cnt + n2_cnt + n3_cnt:
                    combos.append((n0_cnt, n1_cnt, n2_cnt, n3_cnt))

combos.sort(key=lambda x: x[0])
min_num_of_same_nucs_required_per_column = combos[0][0]
max_num_of_diff_nucs_required_per_column = 10-combos[0][0]
print(f'You need at least {min_num_of_same_nucs_required_per_column} of the same nucleotide per column.')
print(f'Which means the max number of incorrect nucleotides per column is {max_num_of_diff_nucs_required_per_column}.')
print(f'Which means the max number of incorrect nucleotides overall is {max_num_of_diff_nucs_required_per_column*15}.')