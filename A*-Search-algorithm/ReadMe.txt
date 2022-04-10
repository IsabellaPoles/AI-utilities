Instruction to run the code: 
The file code that implements the A* Search algorithm is isabella_poles_astar.py

Compiler used to run the code: python 3.7

The code can be run from the command line simply positioning on the current directory where the file is present typing isabella_poles_astar.py, as heuristic manhattan or misplaced, as initial configuration the desired input string. 
Examples: 
python isabella_poles_astar.py 
heuristic: misplaced
initial configuration: 1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12

python isabella_poles_astar.py 
heuristic: manhattan
initial configuration: 1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12

The results for each heuristic are printed in the form of:
- moves leading to the solution
- number of nodes expanded
- total computation time
- total memory usage
Example for the misplaced tiles heuristic, initial configuration 1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12:
heuristic: misplaced
initial configuration: 1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12
A* with misplaced heuristic:
Moves history: ['r', 'u', 'l', 'l', 'd', 'r', 'd', 'r', 'd']
Number of nodes expanded: 22
Total time taken: 0.003245115280151367 s
Total memory usage:  104.0 KB 

Example for the manhattan, initial configuration 1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12:
heuristic: manhattan
initial configuration: 1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12
A* with manhattan heuristic:
Moves history: ['r', 'u', 'l', 'l', 'd', 'r', 'd', 'r', 'd']
Number of nodes expanded: 22
Total time taken: 0.004003286361694336 s
Total memory usage:  76.0 KB