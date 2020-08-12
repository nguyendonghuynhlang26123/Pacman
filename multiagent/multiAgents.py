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
import random, util

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
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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

    def __init__(self, evalFn = 'betterEvaluationFunction', depth='2'):
        self.index = 0 # Pacman is always agent index 0
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
        agent_num = gameState.getNumAgents()
        ActEvalScoreList = []

        """remove stop action from movement list"""
        def removeStopAct(List):
            return [_ for _ in List if _ != 'Stop']
        """recursive minimax"""
        def minimax(node, itercnt):
            """Ending condition"""
            if itercnt >= self.depth*agent_num or node.isWin() or node.isLose():
                """return eval score get from result"""
                return self.evaluationFunction(node)
            if itercnt % agent_num != 0:  # ghost turn (Min node)
                res = 1e10
                for act in removeStopAct(node.getLegalActions(itercnt%agent_num)):
                    successor = node.generateSuccessor(itercnt % agent_num, act)
                    res = min(res, minimax(successor, itercnt+1))
                return res
            else: # Pacman turn (Max node)
                res = -1e10
                for act in removeStopAct(node.getLegalActions(itercnt%agent_num)):
                    successor = node.generateSuccessor(itercnt%agent_num,act)
                    res = max(res, minimax(successor, itercnt+1))
                    if itercnt == 0:
                        ActEvalScoreList.append(res) # add peak node to eval score list
                return res

        res = minimax(gameState, 0)
        # Get act with max eval score from act eval list to return
        return removeStopAct(gameState.getLegalActions(0))[ActEvalScoreList.index(max(ActEvalScoreList))]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agent_num = gameState.getNumAgents()
        ActEvalScoreList = []

        """remove stop action from movement list"""
        def removeStopAct(List):
            return [_ for _ in List if _ != 'Stop']

        def alphabeta(node, itercnt, a, b):
            """Ending condition"""
            if itercnt >= self.depth * agent_num or node.isWin() or node.isLose():
                """return eval score get from result"""
                return self.evaluationFunction(node)
            if itercnt % agent_num != 0:  # ghost turn (Min node)
                res = 1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(itercnt % agent_num, act)
                    res = min(res, alphabeta(successor, itercnt + 1, a, b))
                    b = min(b, res)
                    if b < a:
                        break   # Prune this branch
                return res
            else:  # Pacman turn (Max node)
                res = -1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(itercnt % agent_num, act)
                    res = max(res, alphabeta(successor, itercnt + 1, a, b))
                    a = max(a, res)
                    if itercnt == 0:
                        ActEvalScoreList.append(res)  # add peak node to eval score list
                    if b < a:
                        break   # Prune this branch
                return res

        res = alphabeta(gameState, 0, -1e12, 1e12)
        # Get act with max eval score from act eval list to return
        return removeStopAct(gameState.getLegalActions(0))[ActEvalScoreList.index(max(ActEvalScoreList))]

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
        agent_num = gameState.getNumAgents()
        ActEvalScoreList = []

        def removeStopAct(List):
            return [_ for _ in List if _ != 'Stop']

        def expectimax(node, itercnt):
            if itercnt >= self.depth * agent_num or node.isWin() or node.isLose():
                return self.evaluationFunction(node)
            if itercnt % agent_num != 0:  # Ghost node
                successorScoreList = []
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(itercnt % agent_num, act)
                    res = expectimax(successor, itercnt + 1)
                    successorScoreList.append(res)
                avgscore = sum([score / len(successorScoreList) for score in successorScoreList])
                return avgscore
            else:  # Pacman max
                res = -1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(itercnt % agent_num, act)
                    res = max(res, expectimax(successor, itercnt + 1))
                    if itercnt == 0:
                        ActEvalScoreList.append(res)
                return res

        result = expectimax(gameState, 0)
        return removeStopAct(gameState.getLegalActions(0))[ActEvalScoreList.index(max(ActEvalScoreList))]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def foodheuristic(gameState):
        food_dis = []
        # Find closest food using manhattan distance
        for food in gameState.getFood().asList():
            food_dis.append(1/manhattanDistance(gameState.getPacmanPosition(), food))
        if len(food_dis) > 0:
            return max(food_dis)
        else:
            return 0

    # This is for when pacman is out of hope and he must end his life as soon as possible to reserve his point
    # Testing...
    def bestendingheuristic(gameState):
        ghost_dis = 1e6
        # Find closest ghost using manhattan distance
        for ghost in gameState.getGhostStates():
            ghost_dis = min(manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition()), ghost_dis)
        score = -pow(ghost_dis, 2)
        if gameState.isLose():
            score = 1e6
        return score

    score = currentGameState.getScore()
    foodscore = foodheuristic(currentGameState)
    return score + foodscore
# Abbreviation
better = betterEvaluationFunction

