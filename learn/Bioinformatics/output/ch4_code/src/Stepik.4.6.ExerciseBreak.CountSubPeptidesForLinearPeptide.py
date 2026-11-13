with open('/home/user/Downloads/dataset_240281_3.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

peptide_len = int(data.strip())
subpeptide_count = sum(range(1, peptide_len + 1)) + 1  # + 1 because [] is also considered a subpeptide?

print(f'{subpeptide_count}')