from encapsulator import Encapsulator
from encoder import ProblemInstance
from globals import logger
from parser import ParseArgs
from solverHandler import SolverHandler
from time import perf_counter as clock

def Main():
	try:
		startTime = clock()
		args = ParseArgs()
		N, G, S, R, T = args.N, args.G, args.S, args.R, args.T
		problemInstance = ProblemInstance(N, G, S, R, T)
		solver = SolverHandler(problemInstance)
		Encapsulator(solver.RawResult, N, R, G, S)
		logger.info(f"Finished in {(clock() - startTime):.3f} seconds")
		# Unsolvable - return 1 exit code
		if solver.RawResult.returncode == 20:
			return 1
		# Unsolvable - return 1 exit code else 0 if solvable
		return 1 if solver.RawResult.returncode == 20 else 0
	except Exception as e:
		logger.error(e)
		# Could not finish the program
		return 2

if __name__ == "__main__":
	Main()
