#!/usr/bin/python

import tkinter as tk
from Halma import Halma

class Game(tk.Frame):
    def __init__(self, master=None):
        # Initialize game object and helpers
        self.game = Halma(8, 100, 0)
        self.lastMove = None
        self.legalMoves = self.getLegalMovesForPlayer(self.game.currentMove)
        self.moveFrom = None
        self.moveTo = None
        self.players = [None, "RED", "GREEN"]

        # Grab game assets
        self.PLAYER_GREEN = tk.PhotoImage(file="player_green.png").subsample(2)
        self.PLAYER_RED = tk.PhotoImage(file="player_red.png").subsample(2)
        self.EMPTY = tk.PhotoImage(file="empty.png").subsample(2)
        self.SELECT = tk.PhotoImage(file="select.png").subsample(2)
        self.PAST = tk.PhotoImage(file="past.png").subsample(2)

        # Initialize the Tk window
        super().__init__(master)
        self.pack()
        self.createWidgets()


    def getLegalMovesForPlayer(self, player):
        moveList = []
        for indexI, i in enumerate(self.game.board):
            for indexJ, j in enumerate(i):
                if j == player or j == player + 3:
                    for move in self.game.getLegalMoves(indexI, indexJ):
                        moveList.append(((indexI, indexJ), move))

        return moveList


    def doMove(self, fromX, fromY, toX, toY):
        if ((fromX, fromY), (toX, toY)) in self.legalMoves:
            self.game.makeMove((fromX, fromY), (toX, toY))
            self.lastMove = ((fromX, fromY), (toX, toY))
        self.updateBoard()


    def updateBoard(self):
        for indexI, i in enumerate(self.buttons):
            for indexJ, j in enumerate(i):
                if self.game.board[indexI][indexJ] in [0, 3]:
                    self.buttons[indexI][indexJ].config(image=self.EMPTY)
                    self.buttons[indexI][indexJ].image = self.EMPTY

                elif self.game.board[indexI][indexJ] in [1, 4]:
                    self.buttons[indexI][indexJ].config(image=self.PLAYER_RED) 
                    self.buttons[indexI][indexJ].image = self.PLAYER_RED

                elif self.game.board[indexI][indexJ] in [2, 5]:
                    self.buttons[indexI][indexJ].config(image=self.PLAYER_GREEN) 
                    self.buttons[indexI][indexJ].image = self.PLAYER_GREEN

                if self.lastMove:
                    if (self.lastMove[0], (indexI, indexJ)) == self.lastMove:
                        self.buttons[indexI][indexJ].config(image=self.PAST) 
                        self.buttons[indexI][indexJ].image = self.PAST


    def showLegalMoves(self, x, y):
        # Get a list of coords that are legal moves for x and y
        for i in self.legalMoves:
            if i[0] == (x, y):
                print(i[1])
                self.buttons[i[1][0]][i[1][1]].config(image=self.SELECT)
                self.buttons[i[1][0]][i[1][1]].image = self.SELECT

        print("_____")
        print(self.legalMoves)


    def prepareMove(self, x, y):       
        if self.legalMoves is None:
            return

        if not self.moveFrom:
            self.moveFrom = (x, y)
            self.showLegalMoves(x, y)
            return

        if not self.moveTo:
            for i in self.legalMoves:
                if i == (self.moveFrom, (x, y)):
                    self.moveTo = (x, y)
                    self.doMove(self.moveFrom[0], self.moveFrom[1],
                                self.moveTo[0], self.moveTo[1])
                    self.lastMove = (self.moveTo, self.moveFrom)
                    
                    self.moveTo = None
                    self.moveFrom = None
                    
                    self.updateBoard()
                    
                    self.legalMoves = self.getLegalMovesForPlayer(self.game.currentMove)
                    
                    self.game.checkForWin()
                    
                    if self.game.win == 0:
                        self.status.delete("1.0", tk.END)
                        self.status.insert(tk.INSERT, "Turn: " + self.players[self.game.currentMove])
                    else:
                        self.status.delete("1.0", tk.END)
                        self.status.insert(tk.INSERT, "WIN: " + self.players[self.game.currentMove])
                    return

        self.moveTo = None
        self.moveFrom = None
        self.updateBoard()
        self.prepareMove(x, y)
                

    def createWidgets(self):
        # Create title
        self.title = tk.Text(self, height=1, width=21)
        self.title.insert(tk.INSERT, "Welcome to Halma!")
        self.title.grid(row=0, column=0, columnspan=3)

        self.status = tk.Text(self, height=1, width=14)
        self.status.insert(tk.INSERT, "Turn: " + self.players[self.game.currentMove])
        self.status.grid(row=0, column=len(self.game.board)-2, columnspan=2)

        # Create buttons
        size = len(self.game.board)
        self.buttons = [[-1 for i in range(size)] for j in range(size)]
        for i in range(len(self.game.board)):
            for j in range(len(self.game.board)):
                self.buttons[i][j] = tk.Button(self, width=50, height=50,
                                               text=str(self.game.board[i][j]), 
                                               command=lambda i=i,j=j: self.prepareMove(i, j))
                self.buttons[i][j].grid(column=j, row=i+1, sticky=tk.N+tk.S+tk.E+tk.W)


root = tk.Tk()
app = Game(master=root)
app.mainloop()
