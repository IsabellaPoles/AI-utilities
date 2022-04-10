# CS 411 - Assignment 4 
# Iterative Deepening Depth First Search on 15 Puzzle 
# Isabella Poles UIN 673937460

# The proposed program performs the iterative deepening depth first search to find the solution to any given board position for 15 puzzle, the input should be given in the form of a sequence of numbered tiles for initial board configuration where ‘0’ is indicating the empty space. The outputs will be the number of moves, the number of nodes expanded, the time taken and the memory used. The program is implemented starting from the solution of the breadth-first search provided.  The hash set function is removed and the run_bfs() function is substituded by running the iterative deepening depth first search function run_iddfs() by calling the depth limited search function run_dls() in an iteratively manner.

import random
import math
import time
import psutil
import os
from collections import deque
import sys

# This class defines the state of the problem in terms of board configuration
class Board:
	def __init__(self,tiles):
		self.size = int(math.sqrt(len(tiles))) # defining length/width of the board
		self.tiles = tiles
	
	#This function returns the resulting state from taking particular action from current state
	def execute_action(self,action):
		new_tiles = self.tiles[:]
		empty_index = new_tiles.index('0')
		if action=='L':	
			if empty_index%self.size>0:
				new_tiles[empty_index-1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-1]
		if action=='R':
			if empty_index%self.size<(self.size-1): 	
				new_tiles[empty_index+1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+1]
		if action=='U':
			if empty_index-self.size>=0:
				new_tiles[empty_index-self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-self.size]
		if action=='D':
			if empty_index+self.size < self.size*self.size:
				new_tiles[empty_index+self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+self.size]
		return Board(new_tiles)
		

# This class defines the node on the search tree, consisting of state, parent and previous action		
class Node:
	def __init__(self,state,parent,action):
		self.state = state
		self.parent = parent
		self.action = action
	
	#Returns string representation of the state	
	def __repr__(self):
		return str(self.state.tiles)
	
	#Comparing current node with other node. They are equal if states are equal	
	def __eq__(self,other):
		return self.state.tiles == other.state.tiles
		
            
# Utility function to randomly generate 15-puzzle
def generate_puzzle(size):
	numbers = list(range(size*size))
	random.shuffle(numbers)
	return Node(Board(numbers),None,None)
 
# This function returns the list of children obtained after simulating the actions on current node
def get_children(parent_node):
	children = []
	actions = ['L','R','U','D'] # left,right, up , down ; actions define direction of movement of empty tile
	for action in actions:
		child_state = parent_node.state.execute_action(action)
		child_node = Node(child_state,parent_node,action)
		children.append(child_node)
	return children

# This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
def find_path(node):	
	path = []	
	while(node.parent is not None):
		path.append(node.action)
		node = node.parent
	path.reverse()
	return path

# Runs Depth Limited Search
def run_dls(node, lim):
	if goal_test(node.state.tiles):
		path = find_path(node)
		return path, 0
	elif lim == 0:
		return False, 0
	else:
		expanded_node = 1
		for child in get_children(node):
			path, count_ = run_dls(child, lim - 1)
			expanded_node += count_
			if path != False:
				return path, expanded_node
		return False, expanded_node


# Runs iterative deepening depth first search by calling the depth limited search function in an iteratively manner
def run_iddfs(root_node):
	lim = 1
	start_time = time.time()
	expanded_node = 0
	end_time = time.time()

	while end_time - start_time < 30:
		path, count_ = run_dls(root_node, lim)
		end_time = time.time()
		expanded_node += count_
		if path != False:
			return path, expanded_node, end_time - start_time,  "Solution found:"
		lim += 1

	return None, None, None, "Solution not found:"


# Main function accepting input from console , runnung bfs and showing output
def main():
	process = psutil.Process(os.getpid())
	initial_memory = process.memory_info().rss / 1024.0
	initial = str(input("initial configuration: "))
	initial_list = initial.split(" ")
	root = Node(Board(initial_list), None, None)

	path, expanded_nodes, time_taken, alert = run_iddfs(root)
	print(alert)
	print("Moves history: " + str(path))
	print("Number of nodes expanded: "+ str(expanded_nodes))
	print("Total time taken: " + str(time_taken) + " s")
	final_memory = process.memory_info().rss / 1024.0
	print("Total memory usage: ", str(final_memory - initial_memory) + " KB")


# Utility function checking if current state is goal state or not
def goal_test(cur_tiles):
	return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']


if __name__ == "__main__": main()