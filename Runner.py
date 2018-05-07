#!/usr/bin/python

import tkinter as tk
from Halma import Halma
import Player
import sys

class Game(tk.Frame):
    def __init__(self, master=None):
        # Initialize game object and helpers
        self.aiPlayer = int(sys.argv[1])
        if self.aiPlayer == 1:
            self.game = Halma(8, 1, 0)
        else:
            self.game = Halma(8, 1, 1)

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
                self.buttons[i[1][0]][i[1][1]].config(image=self.SELECT)
                self.buttons[i[1][0]][i[1][1]].image = self.SELECT


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
                        print(self.aiPlayer)
                        if self.game.currentMove == self.aiPlayer:
                            print("Doing AI move...")
                            ai = Player.Player(self.game, self.aiPlayer)
                            self.game = ai.recommendMove(self.game, self.aiPlayer)
                            self.status.delete("1.0", tk.END)
                            self.status.insert(tk.INSERT, "Turn: " + self.players[self.game.currentMove])
                            print("AI move Done")
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
        self.title.grid(row=0, column=1, columnspan=3)

        # Create turn indicator
        self.status = tk.Text(self, height=1, width=14)
        self.status.insert(tk.INSERT, "Turn: " + self.players[self.game.currentMove])
        self.status.grid(row=0, column=len(self.game.board)-2, columnspan=2)

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        self.topIndicators = [-1 for i in range(len(self.game.board))]
        for i in range(len(self.game.board)):
            self.topIndicators[i] = tk.Text(self, height=1, width=1)
            self.topIndicators[i].insert(tk.INSERT, letters[i])
            self.topIndicators[i].grid(row=1, column=i+1, columnspan=1)

        self.sideIndicators = [-1 for i in range(len(self.game.board))]
        for i in range(len(self.game.board)):
            self.sideIndicators[i] = tk.Text(self, height=1, width=1)
            self.sideIndicators[i].insert(tk.INSERT, numbers[i])
            self.sideIndicators[i].grid(row=i+2, column=0, rowspan=1)

        # Create buttons
        size = len(self.game.board)
        self.buttons = [[-1 for i in range(size)] for j in range(size)]
        for i in range(len(self.game.board)):
            for j in range(len(self.game.board)):
                self.buttons[i][j] = tk.Button(self, width=50, height=50,
                                               text=str(self.game.board[i][j]), 
                                               command=lambda i=i,j=j: self.prepareMove(i, j))
                self.buttons[i][j].grid(column=j+1, row=i+2, sticky=tk.N+tk.S+tk.E+tk.W)


root = tk.Tk()
app = Game(master=root)
app.mainloop()
