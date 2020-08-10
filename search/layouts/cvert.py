# %%
import os


def cv(filename):
  if(not os.path.exists(filename)):
    return None
  f = open(filename)
  try:
    maze = ([line.strip() for line in f])
  finally:
    f.close()

  N = len(maze)
  M = len(maze[0])
  pos_pacman = (1, 1)
  grid = []
  char = {'%': '1', ' ': '0', '.': '2', 'G': '3', 'o': '2'}
  for i in range(len(maze)):
    row = []
    for j in range(len(maze[i])):
      if maze[i][j] != 'P':
        row.append(char[maze[i][j]])
      else:
        pos_pacman = (i, j)
        row.append('0')
    grid.append(row)

  grid = '\n'.join(["".join(r) for r in grid])

  s = str(N) + ' ' + str(M) + '\n' + grid + '\n' + \
      str(pos_pacman[0]) + ' ' + str(pos_pacman[1])
  f = open('new/' + filename, 'w')
  try:
    f.write(s)
  finally:
    f.close()


# %%
files = [f for f in os.listdir('.') if os.path.isfile(f) and f != 'cvert.py']
for f in files:
  cv(f)


# %%
