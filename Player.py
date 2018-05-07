import copy
import math
from Halma import Halma

class Player():
    def __init__(self, game, player):
        self.player = player
        self.turn = False
        self.moveTimer = game.tLimit

    def makeMove(self, game):
        #TODO
        return None

    def minimax():
        return

    def rankDistanceFromGoal(self, game, player):
        pawns = self.getPawnLocations(game, player)
        avgDistance = 0
        for pawn in pawns:
            avgDistance += self.avgDistanceFromGoal(game, player, pawn[0], pawn[1])
        return avgDistance/10

    def getPawnLocations(self, game, player):
        pawns = []
        for i in range(0, len(game.board)):
            for j in range(0, len(game.board)):
                if game.board[i][j] == player or game.board[i][j]-3 == player:
                    pawns.append((i,j))
        return pawns

    def avgDistanceFromGoal(self, game, player, x, y):
        winningLocations = self.getWinningLocations(game, player)
        avgDistance = 0
        for location in winningLocations:
            avgDistance += math.sqrt(pow(location[0]-x, 2) + pow(location[1]-y, 2))
        return avgDistance/len(game.board)

    def getWinningLocations(self, game, player):
        winningLocations = []
        if player == 2:
            for i in range(0, 4):
                for j in range(0, 4):
                    if game.board[i][j] == 4:
                        winningLocations.append((i,j))

        elif player == 1:
            for i in range(len(game.board) - 4, len(game.board)):
                for j in range(0, len(game.board)):
                    if game.board[i][j] == 5:
                        winningLocations.append((i,j))

        return winningLocations

class Node:
    def __init__(self, state, scores, minOrMax, parent=None):
        self.state = state
        self.scores = scores
        self.minOrMax = minOrMax
        self.children = []
        self.parent = parent

class MiniMax:
    def __init__(self, rootGameState, player, depth=3):
        # Create root node
        self.player = player
        self.depth = depth
        self.root = Node(rootGameState, (rootGameState.getScore(1), rootGameState.getScore(2)), True)
        self.buildTree(self.root, self.depth)

    def buildTree(self, current, depth):
        if depth == 0:
            return

        # Get the legal moves for the current player
        legalMoves = []
        for indexI, i in enumerate(current.state.board):
            for indexJ, j, in enumerate(i):
                if j in [current.state.currentMove, current.state.currentMove + 3]:
                    # For each legal move, generate a new game state and add it to the children of current
                    for move in current.state.getLegalMoves(indexI, indexJ):
                        newState = copy.deepcopy(current.state)
                        newState.makeMove((indexI, indexJ), (move[0], move[1]))
                        child = Node(newState, (newState.getScore(1), newState.getScore(2)), not current.minOrMax, parent=current)
                        current.children.append(child)

        # Recurse into most likely child
        best = (None, None)

        for i in current.children:
            if i.state.getScore(1) == 10 or i.state.getScore(2) == 10:
                continue
            
            if self.player == 1:
                evaluate = i.state.getScore(1) - i.state.getScore(2)
            else:
                evaluate = i.state.getScore(2) - i.state.getScore(1)
            
            if best[0] == None:
                best = (i, evaluate)
                continue
            elif i.minOrMax and best[1] < evaluate:
                best = (i, evaluate)
                continue
            elif not i.minOrMax and best[1] > evaluate:
                best = (i, evaluate)
                continue
            
            current.children.remove(i)

        self.buildTree(best[0], depth-1)
