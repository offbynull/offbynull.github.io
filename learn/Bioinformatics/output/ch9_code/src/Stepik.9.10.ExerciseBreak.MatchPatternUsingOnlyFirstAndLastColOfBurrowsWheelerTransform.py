# Exercise Break: Match Pattern = "banana" to Text = "panamabananas$" by walking backward through Pattern using the
# Burrows-Wheeler transform of Text.
#
# MY ANSWER
# ---------
# First and last columns are as follows
#
#   [$1, , , , , , , , , , , , ,s1]
#   [a1, , , , , , , , , , , , ,m1]
#   [a2, , , , , , , , , , , , ,n1]
#   [a3, , , , , , , , , , , , ,p1]
#   [a4, , , , , , , , , , , , ,b1]
#   [a5, , , , , , , , , , , , ,n2]
#   [a6, , , , , , , , , , , , ,n3]
#   [b1, , , , , , , , , , , , ,a1]
#   [m1, , , , , , , , , , , , ,a2]
#   [n1, , , , , , , , , , , , ,a3]
#   [n2, , , , , , , , , , , , ,a4]
#   [n3, , , , , , , , , , , , ,a5]
#   [p1, , , , , , , , , , , , ,$1]
#   [s1, , , , , , , , , , , , ,a6]

first_col = [
    ('$', 1),
    ('a', 1),
    ('a', 2),
    ('a', 3),
    ('a', 4),
    ('a', 5),
    ('a', 6),
    ('b', 1),
    ('m', 1),
    ('n', 1),
    ('n', 2),
    ('n', 3),
    ('p', 1),
    ('s', 1)
]

last_col = [
    ('s', 1),
    ('m', 1),
    ('n', 1),
    ('p', 1),
    ('b', 1),
    ('n', 2),
    ('n', 3),
    ('a', 1),
    ('a', 2),
    ('a', 3),
    ('a', 4),
    ('a', 5),
    ('$', 1),
    ('a', 6)
]

#text = 'ana'  # should be True
#text = 'anaf'  # should be False
text = 'banana'  # should be True
found_text = True
found_idxes = [i for i, (ch, idx) in enumerate(first_col) if ch == text[-1]]
for ch in reversed(text[:-1]):
    choices = [last_col[i] for i in found_idxes if last_col[i][0] == ch]
    if len(choices) == 0:
        found_text = False
        break
    found_idxes = [i for i, e in enumerate(first_col) if e in choices]
print(f'{found_text}')


