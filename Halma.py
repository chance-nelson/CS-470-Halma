from pprint import pprint

class Halma:
    def __init__(self, size, tLimit, hPlayer, boardFile=None):
        self.tLimit = 0
        self.hPlayer = 0
        self.board = []
        self.win = 0
        self.currentMove = 1

        # Set up the board
        if size == 8:
            self.board = [[4, 4, 4, 4, 0, 0, 0, 0],
                          [4, 4, 4, 0, 0, 0, 0, 0],
                          [4, 4, 0, 0, 0, 0, 0, 0],
                          [4, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 5],
                          [0, 0, 0, 0, 0, 0, 5, 5],
                          [0, 0, 0, 0, 0, 5, 5, 5],
                          [0, 0, 0, 0, 5, 5, 5, 5]]

        elif size == 10:
            self.board = [[4, 4, 4, 4, 0, 0, 0, 0, 0, 0],
                          [4, 4, 4, 0, 0, 0, 0, 0, 0, 0],
                          [4, 4, 0, 0, 0, 0, 0, 0, 0, 0],
                          [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
                          [0, 0, 0, 0, 0, 0, 0, 0, 5, 5],
                          [0, 0, 0, 0, 0, 0, 0, 5, 5, 5],
                          [0, 0, 0, 0, 0, 0, 5, 5, 5, 5]]

        elif size == 16:
            self.board = [[4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5]]
        
        
        elif boardFile:
            with open(boardFile, "r") as f:
                lineNo = 0
                line = f.readline()
                while line != '':
                    print(lineNo)
                    self.board.append([])
                    self.board[lineNo].append([int(i) for i in line.split(' ')])
                    lineNo += 1
                    line = f.readline()
        
        else:
            raise ValueError("Invalid board size")

        # Set up hPlayer
        if hPlayer >= 0:
            self.hPlayer = hPlayer

        # Set the time limit
        if tLimit > 0:
            self.tLimit = tLimit


    def checkForWin(self):
        counter = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == 5:
                    counter += 1

        if counter == 10:
            self.win = 1
            return True

        counter = 0
        for i in range(len(self.board) - 4, len(self.board) - 1):
            for j in range(0, len(self.board)):
                if self.board[i][j] == 4:
                    counter += 1

        if counter == 10:
            self.win = 2
            return True

        return False 

    
    def getJumps(self, x, y):
        player = self.board[x][y]

        possibleNeighbors = [(x-1, y-1), (x, y-1), (x+1, y), (x+1, y+1),
                            (x, y+1), (x-1, y), (x-1, y+1), (x+1, y-1)]
        
        jumps = []

        i = 0
        while i < len(possibleNeighbors):
            # Prune out invalid spaces
            if possibleNeighbors[i][0] == -1 or possibleNeighbors[i][0] == len(self.board):
                possibleNeighbors.remove(possibleNeighbors[i])
                i = 0
                continue

            if possibleNeighbors[i][1] == -1 or possibleNeighbors[i][1] == len(self.board):
                possibleNeighbors.remove(possibleNeighbors[i])
                i = 0
                continue

            # Prune out neighboring spaces that do not contain a piece
            if self.board[possibleNeighbors[i][0]][possibleNeighbors[i][1]] == 0:
                possibleNeighbors.remove(possibleNeighbors[i])
                i = 0
                continue

            i += 1

        i = 0
        while i < len(possibleNeighbors):
            if possibleNeighbors[i] == (x-1, y-1):
                if 0 <= x-2 < len(self.board) and 0 <= y-2 < len(self.board):
                    if self.board[x-2][y-2] in [0, 3]:
                        jumps.append((x-2, y-2))
 
            if possibleNeighbors[i] == (x, y-1):
                if 0 <= y-2 < len(self.board):
                    if self.board[x][y-2] in [0, 3]:
                        jumps.append((x, y-2))
                  
            if possibleNeighbors[i] == (x+1, y):
                if 0 <= x+2 < len(self.board):
                    if self.board[x+2][y] in [0, 3]:
                        jumps.append((x+2, y))

            if possibleNeighbors[i] == (x+1, y+1):
                if 0 <= x+2 < len(self.board) and 0 <= y+2 < len(self.board):
                    if self.board[x+2][y+2] in [0, 3]:
                        jumps.append((x+2, y+2))

            if possibleNeighbors[i] == (x, y+1):
                if 0 <= y+2 < len(self.board):
                    if self.board[x][y+2] in [0, 3]:
                        jumps.append((x, y+2))

            if possibleNeighbors[i] == (x-1, y):
                if 0 <= x-2 < len(self.board):
                    if self.board[x-2][y] in [0, 3]:
                        jumps.append((x-2, y))
 
            if possibleNeighbors[i] == (x-1, y+1):
                if 0 <= x-2 < len(self.board) and 0 <= y+2 < len(self.board):
                    if self.board[x-2][y+2] in [0, 3]:
                        jumps.append((x-2, y+2))

            if possibleNeighbors[i] == (x+1, y-1):
                if 0 <= x+2 < len(self.board) and 0 <= y-2 < len(self.board):
                    if self.board[x+2][y-2] in [0, 3]:
                        jumps.append((x+2, y-2))

            i = i + 1
    
        return jumps 
 
    def getLegalMoves(self, x, y):
        moveList = [(x, y)]
        
        i = 0
        while i < len(moveList):
            moves = self.getJumps(moveList[i][0], moveList[i][1])
            if moves:
                for move in moves:
                    if move not in moveList:
                        moveList.append(move)
                        
                i = i + len(moves) - 1
            i = i + 1

        possibleMoves = [(x-1, y-1), (x, y-1), (x+1, y), (x+1, y+1),
                         (x, y+1), (x-1, y), (x-1, y+1), (x+1, y-1)]


        moveList.extend(possibleMoves)

        i = 0
        while i < len(moveList):
            if (moveList[i][0] == -1) or (moveList[i][0] == len(self.board)):
                moveList.remove(moveList[i])
                i = 0
                continue

            elif (moveList[i][1] == -1) or (moveList[i][1] == len(self.board)):
                moveList.remove(moveList[i])
                i = 0
                continue

            elif self.board[moveList[i][0]][moveList[i][1]] in [1, 2, 4, 5]:
                moveList.remove(moveList[i])
                i = 0
                continue
            
            i = i + 1
 

        return moveList

    
    def makeMove(self, moveFrom, moveTo):
        if moveTo not in self.getLegalMoves(moveFrom[0], moveFrom[1]):
            raise ValueError("Invalid Move")
        else:
            if self.board[moveFrom[0]][moveFrom[1]] == 4 or self.board[moveFrom[0]][moveFrom[1]] == 5:
                self.board[moveFrom[0]][moveFrom[1]] = 3
            else:
                self.board[moveFrom[0]][moveFrom[1]] = 0

            if self.board[moveTo[0]][moveTo[1]] == 0:
                self.board[moveTo[0]][moveTo[1]] = self.currentMove
            else:
                self.board[moveTo[0]][moveTo[1]] = 3 + self.currentMove

        if self.currentMove == 1:
            self.currentMove = 2
        else:
            self.currentMove = 1
