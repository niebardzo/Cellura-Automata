# Implementation of Celluar Automata method

## What is Celluar Automata (CA)?

The main idea of the cellular automata technique is to divide a specific part of the
material into one-, two-, or three-dimensional lattices of finite cells, where cells have
clearly defined interaction rules between each other. Each cell in this space is called
a cellular automaton, while the lattice of the cells is known as cellular automata
space.

## Grain growth implemetation:

Implementation of grain growth using Moore neighbourhood and absorbing boundary condtion.
In each interation, grain intiallied grow based on self state and states of neighbours from previous timestamp.

## Requirements

All requirements are specified in Pipfile. The best way to install is using **pipenv** being in the folder with Pipfile.

```
pipenv install --dev
pipenv shell
```

Or use standard pip3:

```
pip3 install --requirements
```

## How to run

To run the application we need to start flask server. First export FLASK_APP env variable then you could start flask. Being in the project folder type:

```
export FLASK_APP=server.py
flask run
```

The server should be running on localhost port 5000.


## Application constraints

The maxium table you could create is 300x300. Although the maxium number of grains you could please in the table is 300 but it couldn't be bigger than the biggest dimension. E.g. if you create a table 50x70, the maxium number of grains is 70.

## Endpoints

Currently there are 3 endpoints in the application.

**1. /**

First endpoint of the application takes 2 HTTP method: GET, POST.
- GET returns a webpage with form.
- POST is used to send form data to the backend. As a response you will get redirect to final endpoint with the gif of grain growth and buttons to export png/txt.

**2. /import**

Import endpoint takes also 2 HTTP method: GET, POST.
- GET returns a webpage with form to upload file.
- POST is used to send form data (file) to the backend. As a response you will get redirect to final endpoint with the final image of grown grains and buttons to export png/txt

**3. /final/<file_name>**
This endpoint was design for displaying final results. It is REST Endpoint where you need to give the file name to display a file. If you haven't send any data to the backend before, you will get redirect to main page. 


## Algorytms

### Moore neighbourhood:

The implementation of Moore neighbourhood is one of the methods of CA_space class.
It is called on CA_space object with the input of one cell which is part of the CA_space.
Return the list of cell's neighbours with the cell itself.

```
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
```

![Image of Moore neighbourhood](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Moore_neighborhood_with_cardinal_directions.svg/300px-Moore_neighborhood_with_cardinal_directions.svg.png)



## Contact

If you would like to ask me a question, please contact me: pat049b@gmail.com.
If you are AGH WIMiIP Applied Computer Science student and you found this repository useful in you project, please leave me a star.
