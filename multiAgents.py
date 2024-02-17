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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currentGhostPositions = currentGameState.getGhostPositions()

        "*** YOUR CODE HERE ***"
        Eval = 0
        for i in range(0,len(currentGhostPositions)):
            Eval -= 100*(1/(manhattanDistance(newPos,currentGhostPositions[i]) - 0.999))
        mini = 1000
        for i in range(len(newFood)):
            dist = manhattanDistance(newPos,newFood[i])
            Eval += 20*(1/(dist-0.9))
            if(dist < mini):
                mini = dist
        if mini!=1000:
            Eval += 50*(1/(mini-0.9))
        if currentGameState.hasFood(newPos[0],newPos[1])==True:
            Eval += 10000
        if newPos in currentGhostPositions:
            Eval -= 100000
        x = successorGameState.getLegalActions()
        Eval += 40*len(x)

        if newScaredTimes[0]!=0:
            for i in range(0,len(currentGhostPositions)):
                Eval += 1000000*(1/(manhattanDistance(newPos,currentGhostPositions[i])+0.1))



        #return successorGameState.getScore()
        return Eval

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    minimaxAction = ""

    def minNode(self, gameState, check_depth, agent_num, totalAgents, counter):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        mini = 1000000
        legalMoves = gameState.getLegalActions(agent_num)

        if agent_num == totalAgents-1:
            check_depth += 1
            for i in legalMoves:
                successorState = gameState.generateSuccessor(agent_num, i)
                mini = min(mini, self.maxNode(successorState, check_depth, 0, totalAgents, counter+1))
        else:
            for i in legalMoves:
                successorState = gameState.generateSuccessor(agent_num, i)
                mini = min(mini, self.minNode(successorState, check_depth, agent_num+1, totalAgents, counter+1))

        return mini

    def maxNode(self, gameState, check_depth, agent_num, totalAgents, counter):
        if check_depth==self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        maxi = -1000000
        legalMoves = gameState.getLegalActions(agent_num)
        for i in legalMoves:
            successorState = gameState.generateSuccessor(agent_num, i)
            x = self.minNode(successorState, check_depth, agent_num+1, totalAgents, counter+1)
            if maxi < x:
                if counter==0:
                    self.minimaxAction = i
                maxi = x

        return maxi

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        temp = self.maxNode(gameState, 0, 0, gameState.getNumAgents(), 0)
        return self.minimaxAction

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    minimaxAction = ""

    def minNode(self, gameState, check_depth, agent_num, totalAgents, counter, alpha, beta):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        legalMoves = gameState.getLegalActions(agent_num)
        mini = 1000000
        if agent_num == totalAgents-1:
            check_depth += 1
            for i in legalMoves:
                successorState = gameState.generateSuccessor(agent_num, i)
                x = self.maxNode(successorState, check_depth, 0, totalAgents, counter+1, alpha, beta)
                mini = min(mini,x)
                beta = min(beta,x)
                if alpha > beta:
                    return x
        else:
            for i in legalMoves:
                successorState = gameState.generateSuccessor(agent_num, i)
                x = self.minNode(successorState, check_depth, agent_num+1, totalAgents, counter+1, alpha, beta)
                mini= min(mini,x)
                beta = min(beta,x)
                if alpha > beta:
                    return x

        return mini

    def maxNode(self, gameState, check_depth, agent_num, totalAgents, counter, alpha, beta):
        if check_depth==self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        maxi = -1000000
        legalMoves = gameState.getLegalActions(agent_num)
        for i in legalMoves:
            successorState = gameState.generateSuccessor(agent_num, i)
            x = self.minNode(successorState, check_depth, agent_num+1, totalAgents, counter+1, alpha, beta)
            if maxi < x:
                if counter==0:
                    self.minimaxAction = i
                maxi = x
            alpha = max(alpha,x)
            if alpha > beta:
                return x

        return maxi

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        temp = self.maxNode(gameState, 0, 0, gameState.getNumAgents(), 0, -1000000, 1000000)
        return self.minimaxAction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    expectimaxAction = ""

    def expectiNode(self, gameState, check_depth, agent_num, totalAgents, counter):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        expectation = 0
        legalMoves = gameState.getLegalActions(agent_num)

        if agent_num == totalAgents-1:
            check_depth += 1
            for i in legalMoves:
                successorState = gameState.generateSuccessor(agent_num, i)
                expectation += (self.maxNode(successorState, check_depth, 0, totalAgents, counter+1)/len(legalMoves))
        else:
            for i in legalMoves:
                successorState = gameState.generateSuccessor(agent_num, i)
                expectation += (self.expectiNode(successorState, check_depth, agent_num+1, totalAgents, counter+1)/len(legalMoves))

        return expectation

    def maxNode(self, gameState, check_depth, agent_num, totalAgents, counter):
        if check_depth==self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        maxi = -1000000
        legalMoves = gameState.getLegalActions(agent_num)
        for i in legalMoves:
            successorState = gameState.generateSuccessor(agent_num, i)
            x = self.expectiNode(successorState, check_depth, agent_num+1, totalAgents, counter+1)
            if maxi < x or (maxi==x and self.expectimaxAction=='Stop'):
                if counter==0:
                    self.expectimaxAction = i
                maxi = x

        return maxi

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        temp = self.maxNode(gameState, 0, 0, gameState.getNumAgents(), 0)
        return self.expectimaxAction

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostPos = currentGameState.getGhostPositions()
    capsulePos = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    legalMoves = currentGameState.getLegalActions(0)
    
    if currentGameState.isWin():
        return 1000000
    if currentGameState.isLose():
        return -1000000
    Eval = 0
    Eval -= 100000*len(ghostPos)
    Eval -= 10000*len(foodPos)
    Eval -= 100000*len(capsulePos)
    for g_posi in ghostPos:
        dist = manhattanDistance(pacmanPos,g_posi)
        Eval -= 100*(1/(dist-0.999))   
    mini = 1000000
    for f_posi in foodPos:
        dist = manhattanDistance(pacmanPos,f_posi)
        Eval -= 5*(dist)
        mini = min(mini,dist)
    if mini!=1000000:
        Eval -= 50*(mini)

    return Eval

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
