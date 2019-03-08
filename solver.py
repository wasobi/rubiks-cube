import rubik

def shortest_path(start, end):
	"""
	Using 2-way BFS, finds the shortest path from start_position to
	end_position. Returns a list of moves. 

	You can use the rubik.quarter_twists move set.
	Each move can be applied using rubik.perm_apply
	"""

	moves = rubik.quarter_twists

	# Parent nodes: (Parent_State, move)
	startParents = {}
	startParents[start] = None    # Start state has no parent

	# Parent nodes: (Parent_State, move)
	endParents = {}
	endParents[end] = None        # End state has no parent

	startFrontier = set()    # Current frontier in start BFS
	endFrontier = set()      # Current frontier in end BFS

	startFrontier.add(start) # Add start state as first and only node to generate next frontier
	endFrontier.add(end)     # Add end state as first and only node to generate next frontier

	if end in startParents:
		return []    # Start == End : No moves required

	# We only have to search at most 14 levels in BFS
	# Two-way BFS therefore requires 7 concurrent levels from both states
	for i in range(7):

		startNextFrontier = set()    # New empty set for new frontier to be discovered
		for state in startFrontier:  # Iterate through each rubiks state in this frontier
			for move in moves:       # Apply each move to this state
				nextState = rubik.perm_apply(move, state)

				# Makes sure this new state is not already in the Graph
				# This skips nodes that were already permuted in another path,
				# essentially trimming the Graph's leaves
				if nextState not in startParents:
					startParents[nextState] = (state, move)    # Store this state's parent + move
					startNextFrontier.add(nextState)           # Create a node in the next frontier
				
				# Intersect of both sets, Intermediate state of path found
				if nextState in endParents:
					return solution(startParents, endParents, nextState)

		startFrontier = startNextFrontier    # Make the next frontier the current one

		endNextFrontier = set()      # New empty set for new frontier to be discovered
		for state in endFrontier:    # Iterate through each rubiks state in this frontier
			for move in moves:       # Apply each move to this state
				nextState = rubik.perm_apply(move, state)

				# Makes sure this new state is not already in the Graph
				# This skips nodes that were already permuted in another path,
				# essentially trimming the Graph's leaves
				if nextState not in endParents:
					endParents[nextState] = (state, move)      # Store this state's parent + move
					endNextFrontier.add(nextState)             # Create a node in the next frontier
				
				# Intersect of both sets, Intermediate state of path found
				if nextState in startParents:
					return solution(startParents, endParents, nextState)

		endFrontier = endNextFrontier        # Make the next frontier the current one

	return None

# Returns a list of all moves applied to acquire (Start -> End)
def solution(startParents, endParents, state):
	moves = []    # Array to store sequence of moves
	
	currentState = state    # Intermediate state of rubiks cube
	# Working way back up to start state
	while startParents[currentState] is not None:
		parent = startParents[currentState]    # Parent state + move to current state
		currentState = parent[0]               # Move one level towards initial state
		move = parent[1]                       
		moves.insert(0, move)              # Store moves in FILO (Start -> Intermediate)
	
	currentState = state    # Return to intermediate state of rubiks cube
	# Working way back down to end state
	while endParents[currentState] is not None:
		parent = endParents[currentState]      # Parent state + move to current state
		currentState = parent[0]               # Move on level towards end state
		move = parent[1]
		moves.append(rubik.perm_inverse(move)) # Store inverse of moves in FIFO (Intermediate -> End)

	return moves
