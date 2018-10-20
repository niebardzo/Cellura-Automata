"""Implementation of CA method"""

import datetime
import random
import math

class Cell:

	def __init__(self, ident, timestamp, state):
		self.id = ident
		self.timestamp = timestamp
		self.state = state
		self.previous_timestamp = timestamp
		self.previous_state = state

	
	def find_id(self):
		x , y = self.id.split(':')
		return int(x), int(y)


	def change_state(self, timestamp, state):
		self.previous_state = self.state
		self.previous_timestamp = self.timestamp
		self.timestamp = timestamp
		self.state = state



class CA_space:

	def __init__(self, firstD, secondD, cells):
		time = datetime.datetime.now()
		self.space = [[Cell(str(i)+ ':' + str(j), time, 0) for i in range(secondD)] for j in range(firstD)]
		self.generate_grains(cells)
		self.grains = cells


	def generate_grains(self, cells):
		for cell_num in range(cells):
			sample_row = random.sample(self.space, 1)
			sample_row = sample_row[0]
			sample_cell = random.sample(sample_row, 1)
			sample_cell = sample_cell[0]
			while sample_cell.state != 0:
				sample_row = random.sample(self.space, 1)
				sample_row = sample_row[0]
				sample_cell = random.sample(sample_row, 1)
				sample_cell = sample_cell[0]
			sample_cell.state = cell_num


	def find_neigh(self, cell):
		x , y = cell.find_id()
		neighbours = []
		for row in self.space:
			for c in  row:
				i , j = cell.find_id()
				if math.fabs(x - i) <= 1 and math.fabs(y -j) <= 1:
					neighbours.append(c)
		return neighbours


	def build_grains(self):
		time = datetime.datetime.now()
		for row in self.space:
			for cell in row:
				if cell.state != 0 :
					continue
				else:
					neighbours = self.find_neigh(cell)
					grains = [0 for i in range(self.grains)]
					for i in range(1,self.grains+1):
						for neighbour in neighbours:
							if neighbour.previous_state == i:

								grains[i] = grains[i] + 1
					new_grain = 0
					for i in range(self.grains):
						if grains[i] >= new_grain:
							new_grain = i
					cell.change_state(time, new_grain)





CA = CA_space(20,20,50)
CA.build_grains()