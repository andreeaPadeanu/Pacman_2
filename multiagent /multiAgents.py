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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        emaining food (newFood) and Pacman position after moving (newPos).
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
        
        score = 0

        closestGhostDistance = min(manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates)

        newFoodPositions = newFood.asList()
        if newFoodPositions:
            closestFoodDistance = min(manhattanDistance(newPos, foodPosition) for foodPosition in newFoodPositions)
        else:
            closestFoodDistance = 0

        if action == 'Stop':
            score -= 50

        return successorGameState.getScore() + closestGhostDistance / (closestFoodDistance + 1) + score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            value = float("-inf")
            legalActions = state.getLegalActions(0)  
            for action in legalActions:
                value = max(value, minValue(state.generateSuccessor(0, action), depth, 1))
            return value

        def minValue(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            value = float("inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:
                if agentIndex == gameState.getNumAgents() - 1:
                    value = min(value, maxValue(state.generateSuccessor(agentIndex, action), depth - 1))
                else:
                    value = min(value, minValue(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
            return value

        legalActions = gameState.getLegalActions(0)  
        scores = [minValue(gameState.generateSuccessor(0, action), self.depth, 1) for action in legalActions]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        return legalActions[random.choice(bestIndices)]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            value = float("-inf")
            legalActions = state.getLegalActions(0)  
            for action in legalActions:
                value = max(value, minValue(state.generateSuccessor(0, action), depth, 1, alpha, beta))
                if value > beta:
                    return value
                alpha = max(alpha, value)
            return value

        def minValue(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            value = float("inf")
            legalActions = state.getLegalActions(agentIndex)
            for action in legalActions:
                if agentIndex == gameState.getNumAgents() - 1:
                    value = min(value, maxValue(state.generateSuccessor(agentIndex, action), depth - 1, alpha, beta))
                else:
                    value = min(value, minValue(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value

        legalActions = gameState.getLegalActions(0)  
        alpha = float("-inf")
        beta = float("inf")
        bestAction = None

        for action in legalActions:
            value = minValue(gameState.generateSuccessor(0, action), self.depth, 1, alpha, beta)
            if value > alpha:
                alpha = value
                bestAction = action

        return bestAction



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def expectValue(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            legalActions = state.getLegalActions(agentIndex)
            if agentIndex == gameState.getNumAgents() - 1:
                values = [maxValue(state.generateSuccessor(agentIndex, action), depth - 1) for action in legalActions]
            else:
                values = [expectValue(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1) for action in legalActions]

            return sum(values) / len(values)

        def maxValue(state, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            legalActions = state.getLegalActions(0)  
            values = [expectValue(state.generateSuccessor(0, action), depth, 1) for action in legalActions]
            return max(values)

        legalActions = gameState.getLegalActions(0) 
        scores = [expectValue(gameState.generateSuccessor(0, action), self.depth, 1) for action in legalActions]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        return legalActions[random.choice(bestIndices)]


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPosition = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()

    foodCount = len(foodList)

    ghostDistances = [manhattanDistance(pacmanPosition, ghost.getPosition()) for ghost in ghostStates]
    nearestGhostDistance = min(ghostDistances)

    if foodList:
        nearestFoodDistance = min([manhattanDistance(pacmanPosition, food) for food in foodList])
    else:
        nearestFoodDistance = 0

    scoreWeight = 1.0
    foodCountWeight = -2.0
    ghostDistanceWeight = -5.0
    foodDistanceWeight = -1.0

    evaluation = (
        scoreWeight * score +
        foodCountWeight * foodCount +
        ghostDistanceWeight * nearestGhostDistance +
        foodDistanceWeight * nearestFoodDistance
    )

    return evaluation

better = betterEvaluationFunction
