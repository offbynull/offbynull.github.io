from Read import Read

with open('/home/user/Downloads/dataset_240255_3(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
k = int(lines[0])
text = lines[1]

composition = Read.from_string(text, k)
print('\n'.join([str(x) for x in composition]))