from MedianStringSearch import distance_between_pattern_and_strings
from MotifEnumeration import motif_enumeration

with open('/home/user/Downloads/dataset_240248_1.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
pattern = lines[0].strip()
dnas = lines[1].split(' ')
dnas = [l.strip() for l in dnas] # get rid of whitespace
dnas = [l for l in dnas if len(l) > 0] # get rid of empty lines

dist = distance_between_pattern_and_strings(pattern, dnas)
print(f'{dist}')