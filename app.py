"""Implementation of CA method"""

import datetime
import random
import math
import numpy as np
from prettytable import PrettyTable
from PIL import Image
import imageio
from colour import Color


class Cell:

	def __init__(self, ident, timestamp, state):
		"""Constructor for CELL"""
		self.id = ident
		self.timestamp = timestamp
		self.state = state

	
	def find_id(self):
		"""Method for retriving coordinates in the space for the cell."""
		x , y = self.id.split(':')
		return int(x), int(y)


	def change_state(self, timestamp, state):
		"""Method for changing the state in the cell."""
		self.timestamp = timestamp
		self.state = state



class CA_space:

	def __init__(self, firstD, secondD, cells):
		"""Constructor for CA space. As input you need to give First D size, Second D size and the number of seed grains."""
		self.init_time = datetime.datetime.now()
		self.space = np.array([[Cell(str(i)+ ':' + str(j), self.init_time, 0) for i in range(secondD)] for j in range(firstD)])		
		self.grains = cells + 1
		self.generate_grains(self.grains)
		self.empty_cells = (firstD * secondD) - self.grains


	def generate_grains(self, cells):
		"""Initial method for random placing seed in CA space"""
		for cell_num in range(cells):
			random_row = random.randrange(0,self.space.shape[0],1)
			sample_cell = np.random.choice(self.space[random_row],1)
			sample_cell = sample_cell[0]
			while sample_cell.state != 0:
				random_row = random.randrange(0,self.space.shape[0],1)
				sample_cell = np.random.choice(self.space[random_row],1)
				sample_cell = sample_cell[0]
			sample_cell.change_state(self.init_time ,cell_num)



	def get_neighbours(self, cell):
		"""Method for finding neighbours for inputed cell. Using Moore algorythm and with absorbing boudary condition."""
		x,y = cell.find_id()
		length = self.space.shape[1]
		width = self.space.shape[0]
		if (length == 0 or width == 0 or x < 0 or x >= length or y < 0 or y >= width):
			return []
		neighs = [(i,j) for i in range(y-1,y+2) if 0<=i<width for j in range(x-1,x+2) if 0<=j<length]
		neighbours = []
		for neigh in neighs:
			neighbours.append(self.space[neigh[0],neigh[1]])
		return neighbours


	def check_empty_neighbours(self, cell):
		neighbours = self.get_neighbours(cell)
		flag = True
		for neighbour in neighbours:
			if neighbour.state != 0:
				flag = False
		return flag


	def build_grains(self):
		time = datetime.datetime.now()
		for cell in self.space.flat:
			if cell.state != 0 :
				continue
			elif self.check_empty_neighbours(cell):
				continue
			else:
				neighbours = self.get_neighbours(cell)
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
		"""Will be filling space until all element are not empty."""
		while self.empty_cells >= 0:
			self.build_grains()
			self.pretty_display()

			

	def export_image(self):
		pass

	def export_txt(self):
		pass

	def export_gif(self):
		pass

	def import_image(self):
		pass

	def import_txt(self):
		pass


	def pretty_display(self):
		"""Display the space with PrettyTables."""
		pretty_space = PrettyTable()
		pretty_space.field_names = range(self.space.shape[1])
		count = 0
		pretty_row = []
		for cell in self.space.flat:
			count = count + 1
			pretty_row.append(cell.state)
			if count >= self.space.shape[1]:
				pretty_space.add_row(pretty_row)
				count = 0
				pretty_row = []
		print(pretty_space)


CA = CA_space(30,30,30)
CA.fill_space()
