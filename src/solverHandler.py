from encoder import ProblemInstance
from globals import DEFAULT_SOLVER_OUTPUT_FILE_PATH
import subprocess

class SolverOutput:
	pass

class Solution:
	def __init__(self, solverOutput: SolverOutput):
		pass

class SolverHandler:
	def __init_(self, pi: ProblemInstance):
		self.InputFile = pi.OutputFile
		# TODO: Make configurable output file
		self.OutputFile = DEFAULT_SOLVER_OUTPUT_FILE_PATH


	def CallSolver(self):
		# TODO: Implement
		# return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name], stdout=subprocess.PIPE)
		pass
