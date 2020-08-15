import random
# --------------------------GENERATE MAP---------------------------


# row: num of row, col: num of col
def generate_map(row, col, rate=0.7, numGhosts=0, numFoods=1):
    matrix = []
    empties = []
    total = numGhosts + numFoods + 1
    for i in range(row):
        arr = []
        for j in range(col):
            if (i == 0 or j == 0 or i == row - 1 or j == col - 1):
                arr.append(1)
            else:
                if random.random() >= rate:
                    arr.append(1)
                else:
                    arr.append(0)
                    empties.append((i, j))
        matrix.append(arr)

    if len(empties) < total:
        total = len(empties)
    positions = random.sample(empties, total)
    random.shuffle(positions)

    ghosts_pos = positions[:(numGhosts + 1)]
    foods_pos = positions[(numGhosts + 1):]

    for i, j in ghosts_pos:
        matrix[i][j] = 3
    for i, j in foods_pos:
        matrix[i][j] = 2

    pac_x, pac_y = positions[0]
    matrix[pac_x][pac_y] = 4

    return ["".join([str(c) for c in row]) for row in matrix]
