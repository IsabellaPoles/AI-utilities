# CS 411 - Assignment 6
# Isabella Poles
# UIN 673937460
# Iterative Deepening A* (IDA*) Search on 15 Puzzle
# Based on Sarit Adhikari's Breadth First Search solution

import random
import math
import time
import psutil
import os


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action == 'l':
            if empty_index % self.size > 0:
                new_tiles[empty_index - 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index - 1]
        if action == 'r':
            if empty_index % self.size < (self.size - 1):
                new_tiles[empty_index + 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index + 1]
        if action == 'u':
            if empty_index - self.size >= 0:
                new_tiles[empty_index - self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index - self.size]
        if action == 'd':
            if empty_index + self.size < self.size * self.size:
                new_tiles[empty_index + self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index + self.size]
        return Board(new_tiles)


# This class defines the node on the search tree, consisting of state, parent, previous action and cost function/heuristic values
class Node:
    def __init__(self, state, parent, action, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        if parent is not None:
            self.g = parent.g + 1
        else:
            self.g = 0
        if heuristic == "misplaced":
            self.h = h_misplaced(self.state.tiles)
        elif heuristic == "manhattan":
            self.h = h_manhattan(self.state.tiles)
        else:
            # if no heuristic is provided the algorithm defaults to uniform cost search
            self.h = 0

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles


# Misplaced tiles heuristic
def h_misplaced(tiles):
    dist = 0
    goal = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
    for i in range(len(tiles)):
        if tiles[i] != goal[i]:
            dist += 1
    return dist


# Manhattan heuristic
def h_manhattan(tiles):
    dist = 0
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    for i in range(len(tiles)):
        # the manhathan distance is given by the sum of differences of rows and columns of the considered position and the postion the tile should be in
        dist += abs(i % 4 - goal.index(int(tiles[i])) % 4) + abs(int(i / 4) - int(goal.index(int(tiles[i])) / 4))
    return dist


# Utility function to randomly generate 15-puzzle
def generate_puzzle(size):
    numbers = list(range(size * size))
    random.shuffle(numbers)
    return Node(Board(numbers), None, None)


# This function returns the list of children obtained after simulating the actions on current node
def get_children(parent_node, heuristic):
    children = []
    actions = ['l', 'r', 'u', 'd']  # left,right, up , down ; actions define direction of movement of empty tile
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        child_node = Node(child_state, parent_node, action, heuristic)
        children.append(child_node)
    return sorted(children, key=lambda node: node.g + node.h)


# This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
def find_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path


# Runs Depth Limited A* Search
def run_dls(node, limit, heuristic, explored):
    if goal_test(node.state.tiles):
        path = find_path(node)
        return path, 0, 0, explored
    elif node.g + node.h > limit:
        explored.append(node)
        return False, 0, node.g + node.h, explored
    else:
        nodes_expanded = 1
        explored.append(node)
        min_f = None
        for child in get_children(node, heuristic):
            if child in explored:
                continue
            path, count_, bound, explored = run_dls(child, limit, heuristic, explored)
            nodes_expanded += count_
            if path != False:
                return path, nodes_expanded, 0, explored
            elif min_f is None:
                min_f = bound
            elif bound is None:
                continue
            elif bound < min_f:
                min_f = bound
        return False, nodes_expanded, min_f, explored


# This function runs Iterative Deepening A* search from the given root node and returns path, number of nodes expanded and total time taken
def run_idastar(root_node, heuristic):
    limit = root_node.h
    start_time = time.time()
    nodes_expanded = 0
    end_time = time.time()

    while end_time - start_time < 240:
        path, count_, limit, explored = run_dls(root_node, limit, heuristic, [])
        end_time = time.time()
        nodes_expanded += count_
        if path != False:
            return path, nodes_expanded, end_time - start_time

    return "Solution not found"

# Main function accepting input from console , runnung bfs and showing output
def main():
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024.0
    heuristic = str(input("heuristic: "))
    initial = str(input("initial configuration: "))
    initial_list = initial.split(" ")

    root = Node(Board(initial_list), None, None, heuristic)
    path, count, time_taken = run_idastar(root, heuristic)
    print("IDA* with " + heuristic + " heuristic:")
    print("Moves history: " + str(path))
    print("Number of nodes expanded: "+ str(count))
    print("Total time taken: " + str(time_taken) + " s")
    final_memory = process.memory_info().rss / 1024.0
    print("Total memory usage: ", str(final_memory - initial_memory) + " KB")

# Utility function checking if current state is goal state or not
def goal_test(cur_tiles):
    return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']


if __name__ == "__main__": main()
