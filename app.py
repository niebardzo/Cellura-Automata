"""Implementation of CA method"""

import datetime
import random
import math
import numpy as np

class Cell:

	def __init__(self, ident, timestamp, state):
		self.id = ident
		self.timestamp = timestamp
		self.state = state

	
	def find_id(self):
		x , y = self.id.split(':')
		return int(x), int(y)


	def change_state(self, timestamp, state):
		self.timestamp = timestamp
		self.state = state



class CA_space:

	def __init__(self, firstD, secondD, cells):
		self.init_time = datetime.datetime.now()
		self.space = np.array([[Cell(str(i)+ ':' + str(j), self.init_time, 0) for i in range(secondD)] for j in range(firstD)])
		self.generate_grains(cells)
		self.grains = cells
		self.empty_cells = (firstD * secondD) - self.grains


	def generate_grains(self, cells):
		for cell_num in range(cells):
			random_row = random.randrange(0,self.space.shape[0],1)
			sample_cell = np.random.choice(self.space[random_row],1)
			sample_cell = sample_cell[0]
			while sample_cell.state != 0:
				random_row = random.randrange(0,self.space.shape[0],1)
				sample_cell = np.random.choice(self.space[random_row],1)
				sample_cell = sample_cell[0]
			sample_cell.change_state(self.init_time ,cell_num)


	def find_neigh(self, cell):
		x , y = cell.find_id()
		neighbours = []
		for c in self.space.flat:
			i , j = c.find_id()
			if math.fabs(x - i) <= 1 and math.fabs(y -j) <= 1:
				neighbours.append(c)
		return neighbours


	def build_grains(self):
		time = datetime.datetime.now()
		for cell in self.space.flat:
			if cell.state != 0 :
				continue
			else:
				neighbours = self.find_neigh(cell)
				grains = [0 for i in range(self.grains)]
				for i in range(1,self.grains+1):
					for neighbour in neighbours:
						if neighbour.state == i and neighbour.timestamp < time:
							grains[i] = grains[i] + 1
				if grains == [0 for i in range(self.grains)]:
					continue
				new_grain = 0
				for i in range(self.grains):
					if grains[i] >= new_grain:
						new_grain = i
				cell.change_state(time, new_grain)
				self.empty_cells = self.empty_cells - 1


	def fill_space(self):
		while self.empty_cells > 0:
			self.build_grains()



CA = CA_space(20,20,30)
CA.fill_space()
for row in CA.space:
	for cell in row:
		print("id: ",cell.id,"state: ",cell.state)
		print("id: ", cell.id,"timestamp: ", cell.timestamp)
		print("==============================================")