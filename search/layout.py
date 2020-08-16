# layout.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from functools import reduce
from game import Grid
import os
import random

VISIBILITY_MATRIX_CACHE = {}


class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height = len(layoutText)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.capsules = []
        self.agentPositions = []
        self.numGhosts = 0
        self.processLayoutText(layoutText)
        self.layoutText = layoutText
        self.totalFood = len(self.food.asList())
        # self.initializeVisibilityMatrix()

    def getNumGhosts(self):
        return self.numGhosts

    def initializeVisibilityMatrix(self):
        global VISIBILITY_MATRIX_CACHE
        if reduce(str.__add__, self.layoutText) not in VISIBILITY_MATRIX_CACHE:
            from game import Directions

            vecs = [(-0.5, 0), (0.5, 0), (0, -0.5), (0, 0.5)]
            dirs = [
                Directions.NORTH,
                Directions.SOUTH,
                Directions.WEST,
                Directions.EAST,
            ]
            vis = Grid(
                self.width,
                self.height,
                {
                    Directions.NORTH: set(),
                    Directions.SOUTH: set(),
                    Directions.EAST: set(),
                    Directions.WEST: set(),
                    Directions.STOP: set(),
                },
            )
            for x in range(self.width):
                for y in range(self.height):
                    if self.walls[x][y] == False:
                        for vec, direction in zip(vecs, dirs):
                            dx, dy = vec
                            nextx, nexty = x + dx, y + dy
                            while (nextx + nexty) != int(nextx) + int(
                                nexty
                            ) or not self.walls[int(nextx)][int(nexty)]:
                                vis[x][y][direction].add((nextx, nexty))
                                nextx, nexty = x + dx, y + dy
            self.visibility = vis
            VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)] = vis
        else:
            self.visibility = VISIBILITY_MATRIX_CACHE[
                reduce(str.__add__, self.layoutText)
            ]

    def isWall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def getRandomLegalPosition(self):
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        while self.isWall((x, y)):
            x = random.choice(range(self.width))
            y = random.choice(range(self.height))
        return (x, y)

    def getRandomCorner(self):
        poses = [
            (1, 1),
            (1, self.height - 2),
            (self.width - 2, 1),
            (self.width - 2, self.height - 2),
        ]
        return random.choice(poses)

    def getFurthestCorner(self, pacPos):
        poses = [
            (1, 1),
            (1, self.height - 2),
            (self.width - 2, 1),
            (self.width - 2, self.height - 2),
        ]
        _, pos = max([(manhattanDistance(p, pacPos), p) for p in poses])
        return pos

    def isVisibleFrom(self, ghostPos, pacPos, pacDirection):
        row, col = [int(x) for x in pacPos]
        return ghostPos in self.visibility[row][col][pacDirection]

    def __str__(self):
        return "\n".join(self.layoutText)

    def deepCopy(self):
        return Layout(self.layoutText[:])

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here

        The shape of the maze.  Each character
        represents a different type of object.
         1 - Wall
         2 - Food
         3 - Ghost
         4 - Pacman
        Other characters are ignored.
        """
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)
        self.agentPositions.sort()
        self.agentPositions = [(i == 0, pos) for i, pos in self.agentPositions]

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == "1":  # WALLS
            self.walls[x][y] = True
        elif layoutChar == "2":  # FOODS
            self.food[x][y] = True
        elif layoutChar == "4":  # Pacman
            self.agentPositions.append((0, (x, y)))
        elif layoutChar == "3":  # Ghosts
            self.agentPositions.append((1, (x, y)))
            self.numGhosts += 1


def getLayout(name, back=2):
    if not os.path.exists("layout.py"):
        os.chdir("search/")
    if name.endswith(".txt"):
        layout = tryToLoad("layouts/" + name)
        if layout == None:
            layout = tryToLoad(name)
    else:
        layout = tryToLoad("layouts/" + name + ".txt")
        if layout == None:
            layout = tryToLoad(name + ".txt")
    if layout == None and back >= 0:
        curdir = os.path.abspath(".")
        os.chdir("..")
        layout = getLayout(name, back - 1)
        os.chdir(curdir)
    return layout


def generateMap(n, m, level=1, rate=0.7, numGhosts=0, foodRate=0.33):
    from GM import generate_map

    if level == 1:
        numGhosts = 0
        numFoods = 1
    elif level == 2:
        numFoods = 1
        numGhosts = random.randint(0, int(n * m / 50)) + 1
    elif (level == 3 or level == 4) and numGhosts == 0:
        numGhosts = 2
        numFoods = int(n*m * foodRate)
    elif level > 4 or level < 1:
        raise ("Invalid generate level")
    return Layout(generate_map(n, m, rate, numGhosts=numGhosts, numFoods=numFoods))


def tryToLoad(fullname):
    print(os.getcwd(), fullname)
    if not os.path.exists(fullname):
        return None
    f = open(fullname)
    try:  # LOAD INPUT BASING ON GIVEN FORMAT
        lines = [line.strip() for line in f]
        grid = [list(l) for l in lines[1:-1]]
        pac_pos = lines[-1].split(" ")
        grid[int(pac_pos[0])][int(pac_pos[1])] = "4"
        grid = ["".join(g) for g in grid]
        return Layout(grid)
        # return Layout([line.strip() for line in f])
    finally:
        f.close()
