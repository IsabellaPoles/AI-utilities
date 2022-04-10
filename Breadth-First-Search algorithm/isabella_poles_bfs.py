# 15 puzzle is a sliding puzzle game with numbered squares arranged in 4X4 grid with one tile missing. Starting from a random configuration, the goal is to arrange the tiles in the correct order. Each move on the puzzle is of the form Up/Down/Left/Right. The move "Down" consists of sliding the tile that is above the empty spot downward. The move "Right" consists of sliding a tile to the right, into the empty spot. 
# The proposed program performs a breadth-first search to find the solution to any given board position for 15 puzzle, the input should be given in the form of a sequence of numbered tiles for initial board configuration where ‘0’ is indicating the empty space. The outputs will be the number of moves, the number of nodes expanded, the time taken and the memory used.

# Necessary modules
import numpy as np
import time
from guppy import hpy
import sys


# Definition of the data strcture containing for each state, the previous one and the action that allows to go to the current state. 
# The data structure represents one node of the tree.
class node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# Function used to check if the current state is the goal state. 
def sol_checking(puzzle):
    solved = True
    if puzzle[-1][-1] != 0:
        solved = False
        return solved
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            if i == puzzle.shape[0] - 1 and j == puzzle.shape[1] - 1:
                break
            if puzzle[i][j] != i*4 + j + 1:
                solved = False
                return solved
    return solved


# Function that allows to determine the position expressed in coordinates of the blank space, which is represented as an empty cell. 
def find_vacant(mat):
    for ii in range(mat.shape[0]):
        for jj in range(mat.shape[1]):
            if mat[ii][jj] == 0:
                return ii, jj

            
# Function that allows to perform the action on the given state. The function is returning the new state. 
def state_move(mat, act):
    x_o, y_o = find_vacant(mat)
    x1_o = False
    y1_o = False
    if act == "U":
        y1_o = y_o
        if x_o > 0:
            x1_o = x_o - 1
        else:
            x1_o = 0
    elif act == "D":
        y1_o = y_o
        if x_o < mat.shape[0] - 1:
            x1_o = x_o + 1
        else:
            x1_o = x_o
    elif act == "L":
        x1_o = x_o
        if y_o > 0:
            y1_o = y_o - 1
        else:
            y1_o = y_o
    elif act == "R":
        x1_o = x_o
        if y_o < mat.shape[1] - 1:
            y1_o = y_o + 1
        else:
            y1_o = y_o
    mat1=switch_cells(mat, x_o, y_o, x1_o, y1_o)
    return mat1


# Function that allows to check if a state is already in the closed list, so that it is not expanded and the path is discarded.
def find_repetition(closed_list, state):
    for s in closed_list:
        if np.array_equal(s.state, state):
            return True
        else:
            return False

# Support function that allows to change the position of 2 cells. 
def switch_cells(mat, x, y, xx, yy):
    mat1 = mat.copy()
    tmp = mat[xx][yy]
    mat1[xx][yy] = 0
    mat1[x][y] = tmp
    return mat1


# Support function that allows to convert the input configuration in string type in matrix form. 
def str_2_mat(s):
    mat = np.empty((4,4))
    tmp = s.split()
    for i in range(len(tmp)):
        mat[int(i/4)][i%4] = int(tmp[i])
    return mat


# Function implementing the breadth-fist search algorithm. It returns the path to goal, the nodes expanded, the total time taken and the memory used.
def BFS(mat):
    
    h = hpy()
    
    # Initialization of the data structures
    open_list = []
    open_list.append(node(mat, "", ""))
    closed_list = []
    actions = ["L", "R", "U", "D"]
    nodes_exp = 0

    # Time computation 
    start_time = time.time()
    end_time = time.time()

    # Loop implementing the iterative node search
    while len(open_list) > 0 and (end_time - start_time) < 30:
        current_node = open_list.pop(0)
        if sol_checking(current_node.state):
            end_time = time.time()
            return path_history(current_node), nodes_exp, end_time - start_time, int(h.heap().size / 1024)
        else:
            # Removal of the node from the frontier, children nodes addition to the frontier
            closed_list.append(current_node)
            nodes_exp += 1
            for act in actions:
                new_state = state_move(current_node.state, act)
                # Already visited states are excluded
                if not find_repetition(closed_list, new_state):
                    open_list.append(node(state_move(current_node.state, act), current_node, act))

            # Update time computation 
            end_time = time.time()

    # If the code returns False, a solution was not found
    return False, False, False, False


# Reconstruction of the history path, given the leaf node of the tree
def path_history(node):
    current_node = node
    path = ""
    while current_node.parent != "":
        path = current_node.action + path
        current_node = current_node.parent
    return path


# Main module that takes as input the initial puzzle configuration, it applies the BFS and fially it prints the results. 
def __main__():
    mat = str_2_mat(sys.argv[1])
    path_history, nodes_exp, total_time, total_memory = BFS(mat)
    if path_history != False:
        print("Moves history: " + path_history)
        print("Number of nodes expanded: " + str(nodes_exp))
        print("Total time taken: " + str(total_time) + " s")
        print("Total memory usage: " + str(total_memory) + " kB")
    else:
        print("Solution not found")
        
if __name__ == "__main__":
    __main__()