import numpy as np
from Board import Board
from Node import Node
import math
import random

def uct(node, parentNode):
	if(node.n == 0):
		return(float("inf"))
	return((float(node.w)/node.n) + math.sqrt(2)*math.sqrt((np.log(parentNode.n))/node.n))


def selection(node, l):
	l.append(node)
	if(node.children == [-2 for _ in range(size)] or node.terminal == True):
		return(node.terminal, node)

	first = False
	maxChild = 0
	maxMove = 0
	for child in range(len(node.children)):
		if(node.children[child] != -2):
			uctVal = uct(node.children[child],node) 
			if(first == False):
				maxVal = uctVal
				maxChild = node.children[child]
				maxMove = child
				first = True
			if(uctVal > maxVal):
				maxVal = uctVal
				maxChild = node.children[child]
				maxMove = child
	board.move(maxMove)
	return(selection(maxChild,l))

def play(node):
	result = board.move(random.choice(board.availableMoves()))
	while(isinstance(result,bool)):
		result = board.move(random.choice(board.availableMoves()))
	return(result)

def expansion(node):
	for move in board.availableMoves():
		result = board.move(move)
		if(isinstance(result,bool)):
			node.children[move] = Node(size, False, 0)
		else:
			node.children[move] = Node(size, True, result)
		board.undo(move)

def backprop(l, res):
	for node in range(len(l)):
		if(res == -1):
			if(node%2 == 0):
				l[node].w += 1
		if(res == 1):
			if(node%2 == 1):
				l[node].w += 1
		l[node].n += 1

def bestMove(node):
	first = False
	maxChild = 0
	maxMove = 0
	for child in range(len(node.children)):
		if(node.children[child] != -2):
			val = node.children[child].w
			if(first == False):
				maxVal = val
				maxChild = node.children[child]
				maxMove = child
				first = True
			if(val > maxVal):
				maxVal = val
				maxChild = node.children[child]
				maxMove = child
	return(maxMove)


size = 5
board = Board(size,3)
root = Node(size, False, 0)
expansion(root)
for i in range(5000000):
	if(i%100000 == 0):
		print(i)
	l = []
	res = selection(root, l)
	if(res[0] == True):
		backprop(l, res[1].reward)  
	else:
		expansion(res[1])
		backprop(l,play(res[1]))

	board.reset()