import random
# --------------------------GENERATE MAP---------------------------


def GM_level1(row, col, matrix):
    x = random.randint(1, row-1)
    y = random.randint(1, col-1)
    while (matrix[x][y] != 0):
        x = random.randint(1, row-1)
        y = random.randint(1, col-1)
    matrix[x][y] = 2


def GM_level2(row, col, matrix):
    GM_level1(row, col, matrix)
    count = 0
    for i in range(row):
        for j in range(col):
            if (matrix[i][j] == 0):
                count = count + 1
    count = random.randint(2, int(count/5))
    for i in range(count):
        x = random.randint(1, row-1)
        y = random.randint(1, col-1)
        while (matrix[x][y] != 0):
            x = random.randint(1, row-1)
            y = random.randint(1, col-1)
        matrix[x][y] = 3


def GM_level34(row, col, matrix, numGhosts, numFoods):
    random.seed()
    empties = []
    for i in range(row):
        empties += [(i, j) for j in range(col) if matrix[i][j] == 0]


# row: num of row, col: num of col
def generate_map(row=20, col=20, rate=0.7, numGhosts=0, numFoods=1):
    random.seed()
    matrix = []
    empties = []
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
    total = numGhosts + numFoods + 1
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
