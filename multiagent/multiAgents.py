# multiAgents.py
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


from util import manhattanDistance
from game import Directions
import random
import util
from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        nbAgents = gameState.getNumAgents()
        limit = self.depth * nbAgents

        def minimax(state, curDepth):
            agent = curDepth % nbAgents
            legalActions = [
                act for act in state.getLegalActions(agent) if act != "Stop"
            ]
            if curDepth == limit or not legalActions:
                return self.evaluationFunction(state)
            if agent != 0:  # Ghost turn
                res = 1e10
                for act in legalActions:
                    successor = state.generateSuccessor(agent, act)
                    res = min(res, minimax(successor, curDepth + 1))
                return res
            else:  # Pacman turn
                res = -1e10
                for act in legalActions:
                    successor = state.generateSuccessor(agent, act)
                    score = minimax(successor, curDepth + 1)
                    if res < score:
                        res = score
                        if curDepth == 0:
                            self.__actions = act
                return res

        minimax(gameState, 0)

        return self.__actions


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        nbAgents = gameState.getNumAgents()
        limit = self.depth * nbAgents

        def abPruning(state, curDepth, a, b):
            # Ending condition
            agent = curDepth % nbAgents
            legalActions = [
                act for act in state.getLegalActions(agent) if act != "Stop"
            ]
            if curDepth == limit or not legalActions:
                return self.evaluationFunction(state)
            if agent != 0:  # Ghost turn
                v = 1e10
                for act in legalActions:
                    successor = state.generateSuccessor(agent, act)
                    v = min(v, abPruning(successor, curDepth + 1, a, b))
                    if v < a:
                        return v
                    b = min(b, v)
                return v
            else:  # Pacman turn
                v = -1e10
                for act in legalActions:
                    successor = state.generateSuccessor(agent, act)
                    score = abPruning(successor, curDepth + 1, a, b)
                    if v < score:
                        v = score
                        if curDepth == 0:
                            self.__actions = act
                    if b < v:
                        return v
                    a = max(a, v)
                return v

        abPruning(gameState, 0, -1e12, 1e12)
        return self.__actions


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        nbAgents = gameState.getNumAgents()
        limit = self.depth * nbAgents

        def expectimax(state, curDepth):
            agent = curDepth % nbAgents
            legalActions = [
                act for act in state.getLegalActions(agent) if act != "Stop"
            ]
            if curDepth == limit or not legalActions:
                return self.evaluationFunction(state)
            if agent != 0:  # Ghost node
                sumRes = 0
                for act in legalActions:
                    successor = state.generateSuccessor(agent, act)
                    res = expectimax(successor, curDepth + 1)
                    sumRes += res
                return sumRes / len(legalActions)
            else:  # Pacman max
                res = -1e10
                for act in legalActions:
                    successor = state.generateSuccessor(agent, act)
                    score = expectimax(successor, curDepth + 1)
                    if res < score:
                        res = score
                        if curDepth == 0:
                            self.__actions = act
                return res

        expectimax(gameState, 0)
        return self.__actions


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    def foodHeuristic(gameState):
        food_dis = []
        # Find closest food using manhattan distance
        for food in gameState.getFood().asList():
            food_dis.append(1 / manhattanDistance(gameState.getPacmanPosition(), food))
        if len(food_dis) > 0:
            return max(food_dis)
        else:
            return 0

    # This is for when pacman is out of hope and he must end his life as soon as possible to reserve his point
    # Testing...
    def bestEndingHeuristic(gameState):
        ghost_dis = 1e6
        # Find closest ghost using manhattan distance
        for ghost in gameState.getGhostStates():
            ghost_dis = min(
                manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition()),
                ghost_dis,
            )
        score = -pow(ghost_dis, 2)
        if gameState.isLose():
            score = 1e6
        return score

    def distanceHeuristic(gameState):
        ghost_dis = []
        # Find closest food using manhattan distance
        for g in gameState.getGhostStates():
            ghost_dis.append(
                manhattanDistance(gameState.getPacmanPosition(), g.getPosition())
            )
        if len(ghost_dis) > 0:
            return sum(ghost_dis) / len(ghost_dis)
        else:
            return 0

    score = currentGameState.getScore()
    foodscore = foodHeuristic(currentGameState)
    ghostscore = distanceHeuristic(currentGameState)
    return score + foodscore + ghostscore


def normalEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    def distanceheuristic(gameState):
        ghost_dis = []
        # Find closest food using manhattan distance
        for g in gameState.getGhostStates():
            ghost_dis.append(
                manhattanDistance(gameState.getPacmanPosition(), g.getPosition())
            )
        if len(ghost_dis) > 0:
            return sum(ghost_dis)
        else:
            return 0

    score = currentGameState.getScore()
    ghostscore = distanceheuristic(currentGameState)
    return ghostscore


# Abbreviation
normal = normalEvaluationFunction
better = betterEvaluationFunction
