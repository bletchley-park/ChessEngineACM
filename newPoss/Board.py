import numpy as np

class Board:
	def __init__(self,size, winSize):
		self.winSize = winSize
		self.player = 1
		self.size = size
		self.board = np.zeros(([self.size,self.size]))
	def win(self):
		
		for y in range(self.size): #row
			for x in range(self.size - self.winSize + 1):
				if(self.row(y,x) == True):
					if(self.board[y][x] == 1):
						return(1)
					else:
						return(-1)

		for y in range(self.size - self.winSize + 1): #column
			for x in range(self.size):
				if(self.column(y,x) == True):
					if(self.board[y][x] == 1):
						return(1)
					else:
						return(-1)

		for y in range(self.size - self.winSize + 1): #diag1
			for x in range(self.size - self.winSize + 1):
				if(self.diag1(y,x) == True):
					if(self.board[y][x] == 1):
						return(1)
					else:
						return(-1)

		for y in range(self.size - self.winSize  + 1): #diag2
			for x in range(self.size - self.winSize, self.size):
				if(self.diag2(y,x) == True):
					if(self.board[y][x] == 1):
						return(1)
					else:
						return(-1)

		return(False) ##no win or draw


	def row(self,y,x):
		if(self.board[y][x] == 0):
			return(False)
		for i in range(self.winSize-1):
			if(self.board[y][x+1] != self.board[y][x]):
				return(False)
			x += 1
		return(True)

	def column(self,y,x):
		if(self.board[y][x] == 0):
			return(False)
		for i in range(self.winSize-1):
			if(self.board[y+1][x] != self.board[y][x]):
				return(False)
			y += 1
		return(True)

	def diag1(self,y,x):
		if(self.board[y][x] == 0):
			return(False)
		for i in range(self.winSize-1):
			if(self.board[y+1][x+1] != self.board[y][x]):
				return(False)
			x += 1
			y += 1
		return(True)

	def diag2(self,y,x):
		if(self.board[y][x] == 0):
			return(False)
		for i in range(self.winSize-1):
			if(self.board[y+1][x-1] != self.board[y][x]):
				return(False)
			x -= 1
			y += 1
		return(True)

	def move(self, pos):
		depth = 0
		while(depth+1 < self.size and self.board[depth+1][pos] == 0):
			depth += 1
		self.board[depth][pos] = self.player

		if(self.player == 1):
			self.player = 2
		else:
			self.player = 1

		if(len(self.availableMoves()) == 0):
			if(self.win() == False):
				return(0)
		else:
			return(self.win())

	def undo(self, pos):
		depth = 0
		while(depth+1 < self.size and self.board[depth][pos] == 0):
			depth += 1
		self.board[depth][pos] = 0
		if(self.player == 1):
			self.player = 2
		else:
			self.player = 1

	def reset(self):
		self.board = np.zeros(([self.size,self.size]))
		self.player = 1

	def availableMoves(self):
		moves = []
		for pos in range(self.size):
			if(self.board[0][pos] == 0):
				moves.append(pos)
		return(moves)

	def boardState(self):
		return(self.board)