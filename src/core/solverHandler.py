from encoder import ProblemInstance
from globals import *
import subprocess

class SolverHandler:
	def __init__(self, pi: ProblemInstance, verbosity: int = 1):
		logger.debug("Handing the problem instance to the solver...")
		self._Init(pi, verbosity)
		rawResult = self.CallSolver()
		self.WriteResult(rawResult)
		logger.debug("Finished handling the problem instance.")

	def _Init(self, pi: ProblemInstance, verbosity: int):
		self.InputFile = pi.OutputFile
		# TODO: Make configurable output file + Verbosity
		self.OutputFile = DEFAULT_SOLVER_OUTPUT_FILE_PATH
		# TODO: Better handling but its good enough for now
		if verbosity in [0, 1, 2]:
			self.Verbosity = verbosity
		else:
			raise ValueError(f"Invalid verbosity level: {verbosity}")

	def CallSolver(self):
		with open(self.InputFile) as f:
			command = [
				DEFAULT_SOLVER_EXECUTABLE_PATH,
				"-model",
				"-verb=" + str(self.Verbosity)
			]
			logger.info("Executing SAT solver command: %s", " ".join(command))
			return subprocess.run(command, stdin=f, stdout=subprocess.PIPE)

	def WriteResult(self, result):
		logger.debug(f"Writing SAT solver result to {self.OutputFile}...")
		data = result.stdout.decode("utf-8")
		with open(self.OutputFile, "w") as f:
			f.write(data)

