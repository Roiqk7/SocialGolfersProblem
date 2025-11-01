from encapsulator import Encapsulator
from encoder import ProblemInstance
from globals import logger
from parser import ParseArgs
from solverHandler import SolverHandler
from time import perf_counter as clock

def Main():
	startTime = clock()
	args = ParseArgs()
	N, G, S, R, T = args.N, args.G, args.S, args.R, args.T
	problemInstance = ProblemInstance(N, G, S, R, T)
	solver = SolverHandler(problemInstance)
	Encapsulator(solver.RawResult, N, R, G, S)
	logger.info(f"Finished in {(clock() - startTime):.3f} seconds")

if __name__ == "__main__":
	Main()
