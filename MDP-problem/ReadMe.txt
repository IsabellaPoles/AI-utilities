Input:
The input file describing the MDP has the structure:
- 1st line: number of rows and columns, separated by a space
- 2nd line: The grid positions containing walls, expressed as row and column number separated by a space, separated by commas
- 3rd  line: The grid positions containing terminal states, with the same structure of the wall positions
- 4th line: reward values of terminal states, in the same order as presented in third line, separated by commas
- 5th line: reward value of nonterminal states
- 6th line: transition probabilities with respect to the direction intended, represented as 4 floats separated by a space:
	- 1st value: the probability of going in the direction intended by the action
	- 2nd value: the probability of going right of the direction intended by the action
	- 3rd value: the probability of going right of the direction intended by the action
	- 4th value: the probability of going in the direction opposite to the intended one
- 7th line: discount factor 
- 8th line: epsilon

For example, the input format for the example MDP:
"
5 4
2 2 , 2 3
5 3, 5 4, 4 2
-3, +2, +1
-0.04
0.8 0.1 0.1 0
0.85
0.001
"

The two example inputs provided can be found in the folder in the appropriate format. ('mdp_input.txt' and 'mdp_input_book.txt').

Running the program:
The name of the file from which to parse the MDP should be provided as input by the user (for example'mdp_input.txt').