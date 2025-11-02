from globals import *
from time import perf_counter as clock

class Encapsulator:
	def __init__(self, rawResult, N: int, R: int, G: int, S: int):
		self._Init(rawResult, N, R, G, S)
		# This is the interesting part
		self.ProcessResult()

	def _Init(self, rawResult, N: int, R: int, G: int, S: int):
		"""
		Initializes the encapsulator

		Args:
		rawResult: Raw result from the solver
		N (int): Number of players
		R (int): Number of rounds
		G (int): Number of rounds
		S (int): Size of the groups
		"""
		self._RawResult = rawResult
		self.N = N
		self.R = R
		self.G = G
		self.S = S
		self.InputFile = DEFAULT_SOLVER_OUTPUT_FILE_PATH
		self.OutputFile = PROCESSED_RESULT_PATH
		self.VarIDFile = VAR_ID_FILE_PATH
		self.Vars = []

	def ProcessResult(self):
		"""
		Processes the solver result into a more easily readable format

		The function writes the processed result to a file. If the problem is unsolvable,
		the function just writes "UNSAT". Otherwise it loads variables from a file prepared
		by the encoder, loads the model from the solver and using both of these it rewrites
		the IDs of the vars with their bool values. That makes the vars contain everything
		needed to construct the final format.

		Raises:
		RuntimeError: If anything goes wrong the processing cannot be finished.
		"""
		try:
			startTime = clock()
			logger.debug("Processing result...")
			# 20 is Glucose code for UNSAT
			# in our case that is the trivial case
			if self._RawResult.returncode == 20:
				logger.info(f"Result: UNSAT; Writing into output file: {self.OutputFile}")
				with open(self.OutputFile, "w") as f:
					f.write("UNSAT")
			else:
				# Problem is solvable, so we need to parse it
				logger.info(f"Problem is solvable, constructing a model...")

				# 1. We load the variables self.Vars[i] = [id, r, p, g]
				self._LoadVars()

				# 2. Now we load the model and set self.Vars[i] = [bool, r, p, g]
				self._LoadModel()

				# 3. We filter out options with [False, *, *, *]
				self.Vars = [x for x in self.Vars if x[0]]

				# 4. We sort self.Vars by r and secondarily by g
				self.Vars = sorted(self.Vars, key=lambda var: (var[1], var[3]))

				# 5. Now we construct the final output
				self._FinilizeResult()
			logger.debug(f"Finished result processing in {(clock() - startTime):.3f}.")
		except Exception as e:
			logger.error(e)
			raise RuntimeError(f"Could not process result: {e}")

	def _LoadVars(self):
		"""
		Loads the variables from a file

		In order to correctly parse the model, we need the X variables. But in order to
		identify them we need their IDs. For that reason encoder writes all the X variables
		into a special file with their respective parameters. This function simply reads
		this data and fills the self.Vars with them.

		Raises:
		IOError: If the reading is interrupted, this exception is raised.
		"""
		try:
			with open(self.VarIDFile, "r") as f:
				logger.info(f"Loading variables from file: {self.VarIDFile}")
				for line in f:
					line = line.strip()
					if line:
						id, r, p, g = map(int, line.split())
						self.Vars.append([id, r, p, g])
		except Exception as e:
			logger.error(e)
			raise IOError(f"Could not load variables: {e}")

	def _LoadModel(self):
		"""
		Loads the model from the solver.

		The solver provides a model at a line starting with "v". The line contains
		the IDs with signs as boolean encoding. Negative numbers indicate False and
		positive numbers indicate True.

		Raises:
		IOError: If the reading is interrupted, this exception is raised.
		"""
		try:
			for line in self._RawResult.stdout.decode('utf-8').split('\n'):
				VarsIndex = 0
				if line.startswith("v"):
					vars = line.split(" ")
					vars.pop(0)
					for v in vars:
						v = int(v)
						if abs(v) == self.Vars[VarsIndex][0]:
							# We rewrite the id with the bool value
							self.Vars[VarsIndex][0] = False if v < 0 else True
							VarsIndex += 1
							if VarsIndex >= len(self.Vars):
								break
		except Exception as e:
			logger.error(e)
			raise IOError(f"Could not load model: {e}")

	def _FinilizeResult(self):
		"""
		Writes the result in a desired format.

		After the self.Vars[i] is in the format of [bool, r, p, g], we can
		have everything needed to write the result in the desired format.

		Raises:
		IOError: If the reading is interrupted, this exception is raised.
		"""
		try:
			logger.info(f"Writing model into file: {self.OutputFile}")
			with open(self.OutputFile, "w") as f:
				currentRound = None
				currentGroup = None
				firstInRound = True
				firstInGroup = True

				for b, r, p, g in self.Vars:
					# If we move to a new round
					if r != currentRound:
						if not firstInRound:
							f.write("\n")
						currentRound = r
						currentGroup = None
						firstInRound = False
						firstInGroup = True

					# If we move to a new group
					if g != currentGroup:
						if not firstInGroup:
							f.write(";")
						currentGroup = g
						firstInGroup = False
					else:
						f.write(",")

					# Write player
					f.write(str(p))
		except Exception as e:
			logger.error(e)
			raise IOError(f"Could not write result: {e}")
