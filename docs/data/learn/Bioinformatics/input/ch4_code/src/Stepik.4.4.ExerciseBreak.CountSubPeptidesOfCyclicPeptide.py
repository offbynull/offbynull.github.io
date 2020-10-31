# For now, we will assume for simplicity that the mass spectrometer breaks the copies of a cyclic peptide at every
# possible two bonds, so that the resulting experimental spectrum contains the masses of all possible linear fragments
# of the peptide, which are called subpeptides. For example, the cyclic peptide NQEL has 12 subpeptides: N, Q, E, L,
# NQ, QE, EL, LN, NQE, QEL, ELN, and LNQ. We will also assume that subpeptides may occur more than once if an amino
# acid occurs multiple times in the peptide (e.g., ELEL also has 12 subpeptides: E, L, E, L, EL, LE, EL, LE, ELE, LEL,
# ELE, and LEL.

# l = 4
# print(f'{(l ** 2) - l}')
# l = 31315
# print(f'{(l ** 2) - l}')
# l = 39762
# print(f'{(l ** 2) - l}')

with open('/home/user/Downloads/dataset_240279_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

l = int(data)
print(f'{(l ** 2) - l}')
