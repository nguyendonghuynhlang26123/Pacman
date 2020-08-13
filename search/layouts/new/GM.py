import random
#--------------------------GENERATE MAP---------------------------
def GM_level1(row,col,matrix):
    x = random.randint(1,row-1)
    y = random.randint(1,col-1)
    while (matrix[x][y] != 0):
        x = random.randint(1,row-1)
        y = random.randint(1,col-1)
    matrix[x][y] = 2

def GM_level2(row,col,matrix):
    GM_level1(row,col,matrix)
    count = 0
    for i in range(row):
        for j in range(col):
            if (matrix[i][j] == 0):
                count = count + 1
    count = random.randint(2,int(count/5))
    for i in range(count):
        x = random.randint(1,row-1)
        y = random.randint(1,col-1)
        while (matrix[x][y] != 0):
            x = random.randint(1,row-1)
            y = random.randint(1,col-1)
        matrix[x][y] = 3

def GM_level34(row,col,matrix):
    count = 0
    for i in range(row):
        for j in range(col):
            if (matrix[i][j] == 0):
                count = count + 1
    count = random.randint(5,int(count/3))
    for i in range(2): # food >= 2
        x = random.randint(1,row-1)
        y = random.randint(1,col-1)
        while (matrix[x][y] != 0):
            x = random.randint(1,row-1)
            y = random.randint(1,col-1)
        matrix[x][y] = 2
    for i in range(2): # monster >= 2
        x = random.randint(1,row-1)
        y = random.randint(1,col-1)
        while (matrix[x][y] != 0):
            x = random.randint(1,row-1)
            y = random.randint(1,col-1)
        matrix[x][y] = 3
    for i in range(count-4): # random monster & food
        x = random.randint(1,row-1)
        y = random.randint(1,col-1)
        while (matrix[x][y] != 0):
            x = random.randint(1,row-1)
            y = random.randint(1,col-1)
        matrix[x][y] = random.randint(2,3)

def write_file(matrix,file_name,row,col,x,y):
    f = open(file_name,'w')
    f.write(str(col) + ' ' + str(row))
    f.write("\n")
    for i in range(row):
        for j in range(col):
            f.write(str(matrix[i][j]))
        f.write("\n")
    f.write(str(y+1) + ' ' + str(x+1))
    f.close()

def generate_map(row,col,level,file_name): # row: num of row, col: num of col
    if ((level < 1) or (level > 4)): # check level
        print('Error. Cannot create maps.')
        return

    matrix = []
    for i in range(row):
        arr = []
        for j in range(col):
            if (i == 0 or j ==0 or i == row - 1 or j == col - 1):
                arr.append(1)
            else:
                arr.append(0)
        matrix.append(arr)

    for i in range(int((row-1)*(col-1)/random.randint(3,7))):
        x = random.randint(1,row-1)
        y = random.randint(1,col-1)
        while (matrix[x][y] == 1):
            x = random.randint(1,row-1)
            y = random.randint(1,col-1)
        matrix[x][y] = 1

    if (level == 1):
        GM_level1(row,col,matrix)
    if (level == 2):
        GM_level2(row,col,matrix)
    if ((level == 3) or (level == 4)):
        GM_level34(row,col,matrix)

    x = random.randint(1,row-1)
    y = random.randint(1,col-1)
    while (matrix[x][y] != 0):
        x = random.randint(1,row-1)
        y = random.randint(1,col-1)

    write_file(matrix,file_name,row,col,x,y)
    return file_name

generate_map(20,20,1,"test.txt")