with open('/home/user/Downloads/dataset_240286_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

data = data.strip()

mass_table = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 'D': 115,
              'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186}

prefix_masses = [0]
for i, ch in enumerate(data):
    prev_mass = prefix_masses[i]
    next_mass = prev_mass + mass_table[ch]
    prefix_masses.append(next_mass)
# print(f'{prefix_masses}')

ret = [0]
for k_end in range(0, len(prefix_masses)):
    for k_start in range(0, k_end):
        min_mass = prefix_masses[k_start]
        max_mass = prefix_masses[k_end]
        ret.append(max_mass - min_mass)

ret.sort()
print(f'{" ".join([str(i) for i in ret])}')
