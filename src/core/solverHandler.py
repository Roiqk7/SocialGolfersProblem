from encoder import ProblemInstance
from globals import *
from subprocess import run, PIPE

class SolverHandler:
	def __init__(self, pi: ProblemInstance, verbosity: int = 0):
		try:
			logger.debug("Handing the problem instance to the solver...")
			self._Init(pi, verbosity)
			self.RawResult = self.CallSolver()
			self.WriteResult(self.RawResult)
			logger.debug("Finished handling the problem instance.")
		except Exception as e:
			logger.error(e)
			raise RuntimeError(f"Could not handle the problem instance: {e}")

	def _Init(self, pi: ProblemInstance, verbosity: int):
		self.InputFile = pi.OutputFile
		self.OutputFile = DEFAULT_SOLVER_OUTPUT_FILE_PATH
		if verbosity in [0, 1, 2]:
			self.Verbosity = verbosity
		else:
			logger.warn(f"Invalid verbosity level: {verbosity}. Defaulting to 0.")
			self.Verbosity = 0

	def CallSolver(self):
		try:
			with open(self.InputFile) as f:
				command = [
					DEFAULT_SOLVER_EXECUTABLE_PATH,
					"-model",
					"-verb=" + str(self.Verbosity)
				]
				logger.info("Executing SAT solver command: %s", " ".join(command))
				return run(command, stdin=f, stdout=PIPE)
		except Exception as e:
			logger.error(e)
			raise RuntimeError(f"Could not execute solver: {e}")

	def WriteResult(self, result):
		try:
			logger.info(f"Writing SAT solver result to {self.OutputFile}...")
			data = result.stdout.decode("utf-8")
			with open(self.OutputFile, "w") as f:
				f.write(data)
		except Exception as e:
			logger.error(e)
			raise RuntimeError(f"Could not write result: {e}")
