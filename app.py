"""Implementation of CA method"""

import datetime
import random

class Cell:

	def __init__(self, ident, timestamp, state):
		self.id = ident
		self.timestamp = timestamp
		self.state = state
	
	def find_id(self):
		x , y = self.id.split(':')
		return int(x), int(y)


class CA_space:

	def __init__(self, firstD, secondD, cells):
		time = datetime.datetime.now()
		self.space = [[Cell(str(i)+ ':' + str(j), time, 0) for i in range(secondD)] for j in range(firstD)]
		self.generate_grains(cells)
		self.grains = cells


	def generate_grains(self, cells):
		for cell_num in range(cells):
			sample_cell = random.choice(self.space)
			sample_cell[0].state = cell_num


	def find_neigh(self, cell):
		x , y = cell.find_id()
		try:
			if x > 0 and y > 0 and x < space.length and y < space[0].length:
				return [self.space[x-1][y-1],self.space[x-1][y], self.space[x-1][y+1], self.space[x][y-1], self.space[x][y+1] , self.space[x+1][y-1], self.space[x+1][y], self.space[x+1][y+1]]
			elif x == 0:
				if y == 0:
					return [self.space[x+1][y+1], self.space[x][y+1], self.space[x+1][y+1]]
				elif y < self.space[0].length:
					return [self.space[x][y-1],self.space[x][y+1], self.space[x+1][y],self.space[x+1][y-1], self.space[x+1][y+1]]
				else:
					return [self.space[x-1][y-1], self.space[x-1][y]. self.space[x][y-1]]
			elif x == self.space.length:
				if y == 0:
					return [self.space[x -1][y], self.space[x-1][y+1], self.space[x][y+1]]
				elif y < self.space[0].length:
					return [self.space[x-1][y-1],self.space[x-1][y], self.space[x-1][y+1],self.space[x][y-1],self.space[x][y+1]]
				else:
					return [self.space[x-1][y-1],self.space[x-1][y],self.space[x][y-1]]
			elif y == 0:
				pass
			else:
				pass

		except IndexError:
			return []

	def build_grains(self):
		for row in self.space:
			for cell in row:
				if cell.state != 0 :
					continue
				else:
					neighbours = self.find_neigh(cell)
					if neighbours is []:
						return "Error."
					grains = [0 for i in range(1,self.grains+1)]
					for i in range(1,self.grains+1):
						for neighbour in neighbours:
							if neighbour.state is i:
								grains[i] = grains[i] + 1





space = CA_space(200,200,2)
#space.build_grains()
for row in space.space:
	for cell in row:
		print(cell.state)