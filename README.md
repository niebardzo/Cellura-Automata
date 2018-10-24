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
