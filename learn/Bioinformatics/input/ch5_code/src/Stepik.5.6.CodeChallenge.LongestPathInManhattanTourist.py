with open('/home/user/Downloads/dataset_240301_10.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
n, m = tuple([int(i) for i in lines[0].strip().split()])
down = []
for i in range(1, len(lines)):
    l = lines[i].strip()
    if l == '-':
        break
    row = [int(v) for v in l.split()]
    down.append(row)
right = []
for i in range(i+1, len(lines)):
    l = lines[i].strip()
    if l == '-':
        break
    row = [int(v) for v in l.split()]
    right.append(row)

# create
matrix = [[-1] * (m + 1) for i in range(n + 1)]
matrix[0][0] = 0  # set origin cell to 0
# prime first col
for n_ in range(1, n + 1):
    matrix[n_][0] = matrix[n_ - 1][0] + down[n_ - 1][0]
# prime first row
for m_ in range(1, m + 1):
    matrix[0][m_] = matrix[0][m_ - 1] + right[0][m_ - 1]

# compute remainder of grid
for n_ in range(1, n + 1):
    for m_ in range(1, m + 1):
        down_weight = matrix[n_ - 1][m_] + down[n_ - 1][m_]
        right_weight = matrix[n_][m_ - 1] + right[n_][m_ - 1]
        matrix[n_][m_] = max(down_weight, right_weight)

# for row in matrix:
#     print(f'{row}')
print(f'{matrix[-1][-1]}')