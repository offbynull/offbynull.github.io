# Exercise Break: Play the Three Rocks game using our interactive puzzle (try it online!) and construct the dynamic
# programming table similar to the table above for this game.


# My answer:
# I get the idea here but I don't understand what the conditions are here for win or loss and why its building out like
# it is. That's why I didn't extend this out to 3.
def rocks(n, m):
    R = {}
    R[0, 0] = 'L'
    for i in range(1,n):
        if R[i-1, 0] == 'W':
            R[i, 0] = 'L'
        else:
            R[i, 0] = 'W'
    for j in range(1,m):
        if R[0, j-1] == 'W':
            R[0, j] = 'L'
        else:
            R[0, j] = 'W'
    for i in range(1,n):
        for j in range(1, m):
            if R[i-1,j-1] == 'W' and R[i,j-1] == 'W' and R[i-1,j] =='W':
                R[i,j] = 'L'
            else:
                R[i,j] = 'W'
    return R

table = rocks(10, 10)
for i in range(10):
    for j in range(10):
        print(f'{table[i,j]}', end='')
    print()
