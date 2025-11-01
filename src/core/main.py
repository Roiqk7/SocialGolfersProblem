from encoder import ProblemInstance
from parser import ParseArgs
from solverHandler import SolverHandler

def Main():
	args = ParseArgs()
	N, G, S, R, T = args.N, args.G, args.S, args.R, args.T
	problemInstance = ProblemInstance(N, G, S, R, T)
	solution = SolverHandler(problemInstance)
	return solution

if __name__ == "__main__":
	Main()
