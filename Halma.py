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
        
        else:
            raise ValueError("Invalid board size")

        # Set up hPlayer
        if hPlayer >= 0:
            self.hPlayer = hPlayer

        # Set the time limit
        if tLimit > 0:
            self.tLimit = tLimit

        pprint(self.board)


    def checkForWin(self):
        counter = 0
        for i in range(0, 3):
            for j in i:
                if j == 5:
                    counter += 1

        if counter == 10:
            self.win = 1
            return True

        counter = 0
        for i in range(len(self.board) - 4, len(board) - 1):
            for j in i:
                if j == 4:
                    counter += 1

        if counter == 10:
            self.win = 2
            return True

        return False 

    
    def getJumps(chords):
        x = chords[0]
        y = chords[1]

        player = self.board[x][y]

        possibleNeighbors = [(x-1, y-1), (x, y-1), (x+1, y), (x+1, y+1),
                            (x, y+1), (x-1, y), (x-1, y+1), (x+1, x-1)]
        
        for i in possibleNeighbors:
            # Prune out invalid spaces
            if i[0] == -1 or i[0] == len(self.board):
                possibleNeighbors.remove(i)
                continue

            # Prune out neighboring spaces that do not contain a piece
            if i == 0:
                possibleNeighbors.remove(i)
                continue

            if i == (x-1, y-1):
                if 0 <= x-2 < len(self.board) and 0 <= y-2 < len(self.board):
                    if self.board[x-2][y-2] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue
 
            if i == (x, y-1):
                if 0 <= y-2 < len(self.board):
                    if self.board[x][y-2] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue
                  
            if i == (x+1, y):
                if 0 <= x+2 < len(self.board):
                    if self.board[x+2][y] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue

            if i == (x+1, y+1):
                if 0 <= x+2 < len(self.board) and 0 <= y+2 < len(self.board):
                    if self.board[x+2][y+2] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue

            if i == (x, y+1):
                if 0 <= y+2 < len(self.board):
                    if self.board[x][y+2] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue

            if i == (x-1, y):
                if 0 <= x-2 < len(self.board):
                    if self.board[x-2][y] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue
 
            if i == (x-1, y+1):
                if 0 <= x-2 < len(self.board) and 0 <= y+2 < len(self.board):
                    if self.board[x-2][y+2] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue

            if i == (x+1, y-1):
                if 0 <= x+2 < len(self.board) and 0 <= y-2 < len(self.board):
                    if self.board[x+2][y-2] != 0:
                        possibleNeighbors.remove(i)
                        continue
                else:
                    possibleNeighbors.remove(i)
                    continue

            return possibleNeighbors
 
 
    def getLegalMoves(self, x, y):
        moveList = [(x, y)]

        for i in moveList:
            moveList.extend(self.getJumps(i))

        possibleMoves = [(x-1, y-1), (x, y-1), (x+1, y), (x+1, y+1),
                         (x, y+1), (x-1, y), (x-1, y+1), (x+1, x-1)]

        for i in possibleMoves:
            if i[0] == -1 or i[0] == len(self.board):
                possibleMoves.remove(i)

        moveList.extend(possibleMoves)

    
    def makeMove(self, moveFrom, moveTo):
        if moveTo not in getLegalMoves(moveFrom[0], moveFrom[1]):
            raise ValueError("Invalid Move")
        else:
            if self.board[moveFrom[0]][moveFrom[1]] == 4 or self.board[moveFrom[0]][moveFrom[1]] == 5:
                self.board[moveFrom[0]][moveFrom[1]] = 3
            else:
                self.board[moveFrom[0]][moveFrom[1]] = 0

            if self.board[moveTo[0]][moveTo[1]] == 0:
                self.board[moveTo[0]][moveTo[1]] = self.currentPlayer
            else:
                self.board[moveTo[0]][moveTo[1]] = 3 + self.currentPlayer

        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1
