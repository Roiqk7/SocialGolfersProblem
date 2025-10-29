from encoder import ProblemInstance
from parser import ParseArgs
from solverHandler import SolverHandler

def Main():
	# The way I want this to work is to get just the 5 params and output just a model.
	# The frontend will be responsible for providing the input and also for providing
	# the user with a human readable result.
	#
	# 1. Code the CLI core app
	# 2. Add frontend stuff

	args = ParseArgs()
	N, G, S, R, T = args.N, args.G, args.S, args.R, args.T
	problemInstance = ProblemInstance(N, G, S, R, T)
	solution = SolverHandler(problemInstance) # Might take in and return a class with all the info
	return solution

if __name__ == "__main__":
	Main()
