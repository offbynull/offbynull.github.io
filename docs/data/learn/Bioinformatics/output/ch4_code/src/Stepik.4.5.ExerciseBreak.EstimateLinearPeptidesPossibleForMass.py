# print(f'{exhaust(0, [0] * len(weights_table), 0, 1000)}')  # 8756135919 peptides result in mass of 1000
# print(f'{exhaust(0, [0] * len(weights_table), 0, 1100)}')  # 131791563155 peptides result in mass of 1100


# k*C^mass=peptide_count
#
# eq1: k*C^1000=8756135919
# eq2: k*C^1100=131791563155
#
# k*C^1000*C^100=131791563155            take eq2 and apply product rule on exponent to break up the exponent into two
# 8756135919*C^100=131791563155          replace k*C^1000 with right-hand side of eq1
# C^100=15.0513382129                    divide both sides by 8756135919
# C=1.0274856168086                      take 100th root of 15.051...
#
# k*(1.0274856168086)^1000=8756135919    take eq1 and replace C with the value we got above
# k*596693280597=8756135919              resolve exponent
# k=0.01467443358                        divide both sides by 596693280597

# k*C^mass=peptide_count
# k=0.01467443358
# C=1.0274856168086
#
# 0.01467443358*1.0274856168086^mass=peptide_count

mass = 1200
estimated_peptide_count = 0.01467443358*(1.0274856168086**mass)
print(f'{estimated_peptide_count}')  # for 1200, estimated count=1983639389481.87 vs actual count=1996626917844