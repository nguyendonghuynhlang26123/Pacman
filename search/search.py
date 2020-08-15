# search.py
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    explored = []
    frontier = util.Stack()
    frontier.push((problem.getStartState(), Directions.STOP))
    depth = [0]
    move = []
    while not frontier.isEmpty():
        state, direction = frontier.pop()
        stateDepth = depth.pop()
        explored.append(state)

        move = move[:stateDepth]
        move.append(direction)
        if problem.isGoalState(state):
            return move[1:]

        for successor in problem.getSuccessors(state):
            if successor[0] not in explored:
                frontier.push((successor[0], successor[1]))
                depth.append(stateDepth + 1)
    return None


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    explored = []
    frontier = util.Queue()
    frontier.push((problem.getStartState(), []))
    while not frontier.isEmpty():
        state, move = frontier.pop()
        if problem.isGoalState(state):
            return move
        explored.append(state)
        for successor in problem.getSuccessors(state):
            childState = successor[0]
            if childState not in explored and childState not in (
                item[0] for item in frontier.list
            ):
                newMove = move + [successor[1]]
                frontier.push((childState, newMove))

    return None


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    explored = []
    frontier = util.PriorityQueue()
    frontier.push((start, []), problem.getCostOfActions([]))
    while not frontier.isEmpty():
        state, move = frontier.pop()
        if problem.isGoalState(state):
            return move
        explored.append(state)
        for successor in problem.getSuccessors(state):
            if successor[0] not in explored:
                newMove = move + [successor[1]]
                frontier.update(
                    (successor[0], newMove), problem.getCostOfActions(newMove)
                )
    return None


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    explored = []
    frontier = util.PriorityQueue()
    frontier.push((start, []), problem.getCostOfActions([]))
    while not frontier.isEmpty():
        state, move = frontier.pop()
        if problem.isGoalState(state):
            return move
        explored.append(state)
        for successor in problem.getSuccessors(state):
            childState = successor[0]
            if childState not in explored:
                newMove = move + [successor[1]]
                frontier.update(
                    (childState, newMove),
                    problem.getCostOfActions(newMove) + heuristic(childState, problem),
                )
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
