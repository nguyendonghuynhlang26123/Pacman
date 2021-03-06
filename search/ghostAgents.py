# ghostAgents.py
# --------------
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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance, euclideanHeuristic
import util


def removeStopAct(List):
    return [_ for _ in List if _ != "Stop"]


class GhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        dist = self.getDistribution(state)
        return Directions.STOP if len(dist) == 0 else util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()


class RandomGhost(GhostAgent):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state):
        dist = util.Counter()
        for a in removeStopAct(state.getLegalActions(self.index)):
            dist[a] = 1.0
        dist.normalize()
        # print(state.getLegalActions(self.index), dist)
        return dist


class DirectionalGhost(GhostAgent):
    "A ghost that prefers to rush Pacman"

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack

    def getDistribution(self, state):
        # Read variables from state
        # ghostState = state.getGhostState(self.index)
        legalActions = removeStopAct(state.getLegalActions(self.index))
        pos = state.getGhostPosition(self.index)

        speed = 1

        actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [
            manhattanDistance(pos, pacmanPosition) for pos in newPositions
        ]

        bestScore = min(distancesToPacman) if distancesToPacman != [] else 0
        bestProb = self.prob_attack
        bestActions = [
            action
            for action, distance in zip(legalActions, distancesToPacman)
            if distance == bestScore
        ]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1 - bestProb) / len(legalActions)
        dist.normalize()
        return dist


class LazyGhost(GhostAgent):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state):
        dist = util.Counter()
        dist["Stop"] = 1.0
        return dist


class StupidGhost(GhostAgent):
    "A ghost that Move stupidly"

    def __init__(self, index):
        self.init_pos = ()
        self.index = index
        self.visited = set({})

    def getDistribution(self, state):
        legalActions = removeStopAct(state.getLegalActions(self.index))
        pos = state.getGhostPosition(self.index)
        if self.init_pos == ():
            self.init_pos = pos

        self.visited.add(pos)
        speed = 1
        actionVectors = [Actions.directionToVector(
            a, speed) for a in legalActions]
        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]

        # Select best actions given the state
        distancesToInitialPos = [manhattanDistance(
            pos, self.init_pos) for pos in newPositions]

        bestScore = min(
            distancesToInitialPos) if distancesToInitialPos != [] else 0
        bestActions = [action for action, distance in zip(
            legalActions, distancesToInitialPos) if distance == bestScore]

        dist = util.Counter()
        for a in bestActions:
            dist[a] = 1.0
        dist.normalize()
        # print(state.getLegalActions(self.index), dist)
        return dist
