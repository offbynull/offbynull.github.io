nodes = {
    1: [6, 7, 9],
    2: [8, 3, 10],
    3: [11, 2, 9],
    4: [10, 12],
    5: [7, 11],
    6: [8, 12, 1],
    7: [12, 1, 5],
    8: [2, 6],
    9: [3, 1],
    10: [2, 11, 4],
    11: [5, 10, 3],
    12: [4, 6, 7]
}

def tour(path):
    n = path[-1]
    for child_n in nodes[n]:
        if child_n == path[0] and len(path) + 1 == len(nodes):
            print(f'{path}')
        elif child_n not in path:
            path.append(child_n)
            tour(path)
            path.pop()


tour([1])