"""Implementation of CA method"""

import datetime
import random
import math
import numpy as np
from prettytable import PrettyTable
from PIL import Image
import imageio
from colour import Color
import os
from shutil import copyfile


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


	def get_neighbours_round(self, cell, radius):
		"""Method for finding neighbours for inputed cell. Based on Moore algorythm but trying to generete round with radius inputted and with absorbing boudary condition."""
		x,y = cell.find_id()
		
		length = self.space.shape[1]
		width = self.space.shape[0]
		if (length == 0 or width == 0 or x < 0 or x >= length or y < 0 or y >= width or radius < 2):
			return []
		neighs = [(i,j) for i in range(y-radius,y+radius+1) if 0<=i<width for j in range(x-radius,x+radius+1) if (0<=j<length)]
		neighbours = []
		for neigh in neighs:
			i , j = neigh
			if round(math.sqrt((j-x)**2+(i-y)**2),4) <= round(radius + math.sqrt(1),4):
				neighbours.append(self.space[neigh[0],neigh[1]])
		return neighbours


	def check_empty_neighbours(self, cell):
		"""To check if cell has only neighbours with the state 0."""
		neighbours = self.get_neighbours(cell)
		flag = True
		for neighbour in neighbours:
			if neighbour.state != 0:
				flag = False
		return flag


	def build_grains(self):
		"""Basic function to grow the grains."""
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


	def fill_space(self, name, inclusions):
		"""Will be filling space until all element are not empty."""
		inc_n, inc_p, inc_r = inclusions
		counter = 0
		self.export_image(str(name)+str(counter))
		while self.empty_cells >= 0:
			self.build_grains()
			counter = counter + 1
			self.export_image(str(name)+str(counter))
			#self.pretty_display()

		# Inclusion added
		if inc_n > 0:
			if inc_p is True:
				self.generate_inclusions_randomly(inc_n,inc_r)
			else:
				self.generate_inclusions_on_boundary(inc_n,inc_r)

		## 5 time export image to gif to better visualize inclusion
		counter = counter + 1
		self.export_image(str(name)+str(counter))
		counter = counter + 1
		self.export_image(str(name)+str(counter))
		counter = counter + 1
		self.export_image(str(name)+str(counter))
		counter = counter + 1
		self.export_image(str(name)+str(counter))
		counter = counter + 1
		self.export_image(str(name)+str(counter))
		#
		#
		self.export_image(name)
		self.export_txt(name)
		copyfile('./static/temp/'+str(name)+'.png', './static/temp/temp.png')
		out = open('./static/temp/'+str(name)+'.png', 'wb')
		out.write(open('./static/temp/temp.png', 'rb').read())
		out.write('\n'.encode('utf-8'))
		out.write(open('./static/temp/'+str(name)+'.txt', "rb").read())
		out.close()
		os.remove('./static/temp/temp.png')
		self.export_gif(name,counter)

			
	def export_txt(self, name):
		with open('./static/temp/'+str(name)+'.txt','w') as file:
			file.write(str(self.space.shape[1])+ ' ' + str(self.space.shape[0])+' '+str(self.grains - 1) + '\n')
			for cell in self.space.flat:
				x, y = cell.find_id()
				file.write(str(x)+' '+str(y)+' '+str(cell.state)+' '+str(cell.id)+'\n')				


	def export_image(self, name):
		"""One cell for 9 pixels. Colors of grains from red to blue."""
		red = Color("red")
		blue = Color("blue")
		white = Color("white")
		black = Color("black")
		rgb_black = []
		for part in black.rgb:
			part = part * 255
			rgb_black.append(part)
		rgb_white = []
		for part in white.rgb:
			part = part * 255
			rgb_white.append(part)
		colours = list(red.range_to(blue, int(self.grains)))
		image = np.zeros([self.space.shape[1],self.space.shape[0], 3], dtype=np.uint(8))
		for grain in range(self.grains+1):
			rgb = []
			for part in colours[grain-1].rgb:
				part = part * 255
				rgb.append(part)
			for cell in self.space.flat:
				if cell.state == grain:
					x,y = cell.find_id()
					image[x,y] = rgb
				if cell.state == 999:
					x,y = cell.find_id()
					image[x,y] = rgb_black
		img = Image.fromarray(image.astype('uint8'))
		img = img.resize((self.space.shape[1]*3,self.space.shape[0]*3))
		img.save('./static/temp/'+str(name)+'.png')


	def export_gif(self,name,counter):
		images = []
		if counter == 0:
			counter = 1
		for i in range(0,counter):
			images.append(imageio.imread('./static/temp/'+str(name)+str(i)+'.png'))
		if images == []:
			return 0
		imageio.mimsave('./static/temp/'+str(name)+'.gif', images)
		for i in range(counter):
			os.remove('./static/temp/'+str(name)+str(i)+'.png')


	def import_txt(self, name):
		with open('./static/temp/'+str(name), 'r') as file:
			lines = file.readlines()
			init = lines[0].split(' ')
			self.__init__(int(init[1]),int(init[0]),int(init[2]))
			self.empty_cells = -1
			for line in lines[1:]:
				line = line.split(' ')
				self.space[int(line[1]),int(line[0])].state = int(line[2])


	def pretty_display(self):
		"""Display the space with PrettyTables. Used for testing purpose before export was avaiable."""
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


	def check_for_inclusions(self, cell, radius):
		neighbours = self.get_neighbours_round(cell,radius+1)
		for cell in neighbours:
			if cell.state == 999:
				return True
		return False


	def grow_cell_inclusion(self,cell,timestamp,radius):
		neighbours = self.get_neighbours_round(cell, radius)
		for neighbour in neighbours:
			neighbour.change_state(timestamp,999)


	def find_boudary_cell(self, radius):
		length = self.space.shape[1]
		width = self.space.shape[0]
		sample_cell = 0
		while sample_cell == 0:
			random_cell = np.random.choice(self.space.flat,1)
			random_cell = random_cell[0]
			neighbours = self.get_neighbours(random_cell)
			for neighbour in neighbours:
				if neighbour.state != random_cell.state:
					sample_cell = random_cell
					break
			if sample_cell != 0:
				break
		x , y = sample_cell.find_id()
		while (x-radius < 0 and x+radius >= length and y-radius < 0 and y+radius >= width):
			sample_cell = 0
			while sample_cell == 0:
				random_cell = np.random.choice(self.space.flat,1)
				random_cell = random_cell[0]
				neighbours = self.get_neighbours(random_cell)
				for neighbour in neighbours:
					if neighbour.state != random_cell.state:
						sample_cell = random_cell
						break
				if sample_cell != 0:
					break
			x , y = sample_cell.find_id()
		return sample_cell


	def find_random_cell(self, radius):
		length = self.space.shape[1]
		width = self.space.shape[0]
		sample_cell = np.random.choice(self.space.flat,1)
		sample_cell = sample_cell[0]
		x , y = sample_cell.find_id()
		while (x-radius < 0 and x+radius >= length and y-radius < 0 and y+radius >= width):
			sample_cell = np.random.choice(self.space.flat,1)
			sample_cell = sample_cell[0]
			x, y = sample_cell.find_id()
		return sample_cell


	def find_boundary_cell_for_inculsion(self,radius):
		cell = self.find_boudary_cell(radius)
		while self.check_for_inclusions(cell,radius):
			cell = self.find_boudary_cell(radius)
		return cell

	def find_cell_for_inclusion(self, radius):
		cell = self.find_random_cell(radius)
		while self.check_for_inclusions(cell, radius):
			cell = self.find_random_cell(radius)
		return cell


	def generate_inclusions_randomly(self, number,radius):
		start, stop = radius
		now = datetime.datetime.now()
		for i in range(number):
			if start == stop:
				rad = start
			else:
				rad = random.choice(range(start,stop+1))
			inclusion = self.find_cell_for_inclusion(rad)
			self.grow_cell_inclusion(inclusion, now,rad)
			

	def generate_inclusions_on_boundary(self, number,radius):
		start, stop = radius
		now = datetime.datetime.now()
		for i in range(number):
			if start == stop:
				rad = start
			else:
				rad = random.choice(range(start,stop+1))
			inclusion = self.find_boundary_cell_for_inculsion(rad)
			self.grow_cell_inclusion(inclusion, now,rad)


#CA = CA_space(200,200,50)
#CA.import_txt("import.txt")
#CA.fill_space("export")