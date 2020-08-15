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
from searchAgents import shortestPathFrom
from game import Agent, Actions


def removeStopAct(List):
    return [_ for _ in List if _ != 'Stop']


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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

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

    def __init__(self, evalFn='defaultEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def foodEval(self, gameState):
        closestFood = gameState.getClosestFood()
        if closestFood == None or closestFood in self.unreachableFoods:
            return 0
        disClosestFood = manhattanDistance(
            gameState.getPacmanPosition(), gameState.getClosestFood())
        current_score = gameState.getScore()
        foodsLeft = gameState.getNumFood()
        return current_score - 1.5 * disClosestFood - 4*foodsLeft

    def ghostEval(self, gameState):
        if gameState.getClosestGhost() == None:
            return 0
        distToClosestGhost = manhattanDistance(
            gameState.getPacmanPosition(), gameState.getClosestGhost())
        if (distToClosestGhost == 0):
            return -99999
        return - 2*(1.0/distToClosestGhost)

    def combinedEval(self, gameState):
        return self.foodEval(gameState) + self.ghostEval(gameState)


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

        """recursive minimax"""
        def minimax(node, itercnt):
            """Ending condition"""
            if itercnt >= self.depth*agent_num or node.isWin() or node.isLose():
                """return eval score get from result"""
                return self.evaluationFunction(node)
            if itercnt % agent_num != 0:  # ghost turn (Min node)
                res = 1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(
                        itercnt % agent_num, act)
                    res = min(res, minimax(successor, itercnt+1))
                return res
            else:  # Pacman turn (Max node)
                res = -1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(
                        itercnt % agent_num, act)
                    res = max(res, minimax(successor, itercnt+1))
                    if itercnt == 0:
                        # add peak node to eval score list
                        ActEvalScoreList.append(res)
                return res

        minimax(gameState, 0)
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

        def AlphaBeta(node, itercnt, alpha, beta):
            """Ending condition"""
            if itercnt >= self.depth * agent_num or node.isWin() or node.isLose():
                """return eval score get from result"""
                return self.evaluationFunction(node)
            if itercnt % agent_num != 0:  # ghost turn (Min node)
                res = 1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(
                        itercnt % agent_num, act)
                    res = min(res, alphabeta(successor, itercnt + 1, alpha, beta))
                    beta = min(beta, res)
                    if res <= alpha:
                        break   # Prune this branch
                return res
            else:  # Pacman turn (Max node)
                res = -1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(
                        itercnt % agent_num, act)
                    res = max(res, alphabeta(successor, itercnt + 1, alpha, beta))
                    alpha = max(alpha, res)
                    if itercnt == 0:
                        # add peak node to eval score list
                        ActEvalScoreList.append(res)
                    if res >= beta:
                        break   # Prune this branch
                return res

        res = AlphaBeta(gameState, 0, -1e10, 1e10)
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

        def expectimax(node, itercnt):
            if itercnt >= self.depth * agent_num or node.isWin() or node.isLose():
                return self.evaluationFunction(node)
            if itercnt % agent_num != 0:  # Ghost node
                successorScoreList = []
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(
                        itercnt % agent_num, act)
                    res = expectimax(successor, itercnt + 1)
                    successorScoreList.append(res)
                avgscore = sum([score / len(successorScoreList)
                                for score in successorScoreList])
                return avgscore
            else:  # Pacman max
                res = -1e10
                for act in removeStopAct(node.getLegalActions(itercnt % agent_num)):
                    successor = node.generateSuccessor(
                        itercnt % agent_num, act)
                    res = max(res, expectimax(successor, itercnt + 1))
                    if itercnt == 0:
                        ActEvalScoreList.append(res)
                return res

        expectimax(gameState, 0)
        return removeStopAct(gameState.getLegalActions(0))[ActEvalScoreList.index(max(ActEvalScoreList))]


class ExplorerAgent(ExpectimaxAgent):
    def __init__(self, miracle_rate=0.001):
        self.guide = []
        self.miracle_turns = 0
        self.miracle_rate = miracle_rate
        self.explored = set({})
        self.unreachableFoods = set({})
        super(ExplorerAgent, self).__init__()

    def exploreActions(self, position, legalActions):
        """
            Return the action lead to the uneplored square
        """
        directions = {a: Actions.getSuccessor(
            position, a) for a in legalActions}
        result = [k for k in directions.keys() if directions[k]
                  not in self.explored]
        return result if result != [] else legalActions

    def getAction(self, gameState):
        perceived_ghosts = gameState.getGhostSurroundingPacman(radius=3)
        perceived_foods = gameState.getFoodSurroundingPacman(radius=3)
        legalActions = self.exploreActions(gameState.getPacmanPosition(),
                                           removeStopAct(gameState.getLegalActions(0)))
        closest_Food = gameState.getClosestFood()
        self.explored.add(gameState.getPacmanPosition())

        if (len(perceived_ghosts) == 0 and len(perceived_foods) == 0):
            "MIRACLE: "
            if len(self.guide) > 0 or (gameState.getScore() < 0 and random.random() > self.miracle_rate):
                print("MIRACLE")
                next_step = self.miracleGuide(gameState)
                if next_step is not None:
                    return next_step
            print("random")
            return random.choice(legalActions)
        elif len(perceived_ghosts) == 0:
            "SAW ONLY FOOD"
            self.guide = []
            print("F", perceived_foods)
            if closest_Food != None:
                path = shortestPathFrom(
                    gameState.getPacmanPosition(), closest_Food, gameState)
                if path == None:
                    return random.choice(legalActions)
                else:
                    return path[0]
            return random.choice(legalActions)
        elif len(perceived_foods) == 0:
            "SAW ONLY GHOST"
            self.guide = []
            print("GHOST")
            self.evaluationFunction = self.ghostEval
        else:
            "SAW BOTH FOOD AND GHOST"
            self.guide = []
            print("F&G")
            self.evaluationFunction = default

        return super(ExplorerAgent, self).getAction(gameState)

    def miracleGuide(self, gameState):
        closest_Food = gameState.getClosestFood()
        if (self.guide == [] and closest_Food not in self.unreachableFoods):
            self.guide = shortestPathFrom(
                gameState.getPacmanPosition(), closest_Food, gameState)
            if self.guide is None:
                self.unreachableFoods.add(closest_Food)
                self.guide = []
        return self.guide.pop(0) if self.guide != [] else None


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
            food_dis.append(
                1/manhattanDistance(gameState.getPacmanPosition(), food))
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
            ghost_dis = min(manhattanDistance(
                gameState.getPacmanPosition(), ghost.getPosition()), ghost_dis)
        score = -pow(ghost_dis, 2)
        if gameState.isLose():
            score = 1e6
        return score

    def distanceheuristic(gameState):
        ghost_dis = []
        # Find closest food using manhattan distance
        for g in gameState.getGhostStates():
            ghost_dis.append(
                manhattanDistance(gameState.getPacmanPosition(), g.getPosition()))
        if len(ghost_dis) > 0:
            return (sum(ghost_dis) / len(ghost_dis))
        else:
            return 0

    score = currentGameState.getScore()
    foodscore = foodheuristic(currentGameState)
    ghostscore = distanceheuristic(currentGameState)
    return score + foodscore + ghostscore


def customEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def distanceToClosestGhost(gameState):
        ghosts = gameState.getGhostPositions()
        ghosts_dis = [manhattanDistance(
            gameState.getPacmanPosition(), g) for g in ghosts]
        if (min(ghosts_dis) == 0):
            return -9999
        return min(ghosts_dis)

    # https://www.dcalacci.net/2013/pacman-gradient-descent/
    closestFood = manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getClosestFood())
    current_score = currentGameState.getScore()
    distToClosestGhost = distanceToClosestGhost(currentGameState)
    foodsLeft = currentGameState.getNumFood()

    return current_score - 1.5 * closestFood - 2*(1.0/distToClosestGhost) - 4*foodsLeft


def defaultEvaluationFunction(currentGameState):
    def foodheuristic(gameState):
        # Find closest food using manhattan distance
        foods = gameState.getFoodSurroundingPacman(2)
        food_dis = ([manhattanDistance(gameState.getPacmanPosition(), food)
                     for food in foods])
        return min(food_dis) if food_dis != [] else 0

    # This is for when pacman is out of hope and he must end his life as soon as possible to reserve his point
    # Testing...
    def bestendingheuristic(gameState):
        ghost_dis = 1e6
        # Find closest ghost using manhattan distance
        for ghost in gameState.getGhostStates():
            ghost_dis = min(manhattanDistance(
                gameState.getPacmanPosition(), ghost.getPosition()), ghost_dis)
        score = -pow(ghost_dis, 2)
        if gameState.isLose():
            score = 1e6
        return score

    def distanceheuristic(gameState):
        ghost_dis = []
        # Find closest food using manhattan distance
        for g in gameState.getGhostStates():
            ghost_dis.append(manhattanDistance(gameState.getPacmanPosition(), g.getPosition()))
        if len(ghost_dis) > 0:
            return (sum(ghost_dis) / len(ghost_dis))
        else:
            return 0

    score = currentGameState.getScore()
    foodscore = foodheuristic(currentGameState)
    ghostscore = distanceheuristic(currentGameState)
    if score < -600 and len(currentGameState.getFoodSurroundingPacman(3)) <= 1:
        print('SUICIDE')
        return bestendingheuristic(currentGameState)
    return score - 1.5*foodscore - 4*ghostscore



# Abbreviation
default = defaultEvaluationFunction     # Use this eval func
custom = customEvaluationFunction
better = betterEvaluationFunction
