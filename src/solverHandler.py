from encoder import ProblemInstance

class SolverOutput:
	pass

class Solution:
	def __init__(self, solverOutput: SolverOutput):
		pass

def HandleSolver(input: ProblemInstance) -> Solution:
	try:
		solverOutput = CallSolver()
	except Exception as e:
		pass

	return Solution(solverOutput)


def CallSolver():
	return SolverOutput()
