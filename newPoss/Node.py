class Node:
	def __init__(self, size, terminal, result):
		self.n = 0
		self.w = 0
		self.terminal = terminal
		self.children = [-2 for _ in range(size)]
		self.reward = result