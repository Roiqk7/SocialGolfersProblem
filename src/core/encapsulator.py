from globals import *
from time import perf_counter as clock

class Encapsulator:
	def __init__(self, rawResult, N: int, R: int, G: int, S: int):
		self._RawResult = rawResult
		self.N = N
		self.R = R
		self.G = G
		self.S = S
		self.InputFile = DEFAULT_SOLVER_OUTPUT_FILE_PATH
		self.OutputFile = PROCESSED_RESULT_PATH
		self.VarIDFile = VAR_ID_FILE_PATH
		self.Vars = []

		# This is the interesting part
		self.ProcessResult()

	def ProcessResult(self):
		startTime = clock()
		logger.debug("Processing result...")
		# 20 is Glucose code for UNSAT
		# in our case that is the trivial case
		if self._RawResult.returncode == 20:
			logger.info(f"Result: UNSAT; Writing into output file: {self.OutputFile}")
			with open(self._RawResult, "w") as f:
				f.write("UNSAT")
				return
		# Problem is solvable, so we need to parse it
		logger.debug(f"Problem is solvable, constructing a model...")

		# 1. We load the variables self.Vars[i] = [id, r, p, g]
		self._LoadVars()

		# 2. Now we load the model and set self.Vars[i] = [bool, r, p, g]
		self._LoadModel()

		# 3. We filter out options with [False, *, *, *]
		self.Vars = [x for x in self.Vars if x[0]]

		# 4. We sort self.Vars by r and secondarily by g
		self.Vars = sorted(self.Vars, key=lambda var: (var[1], var[3]))

		# 5. Now we construct the final output
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
		logger.debug(f"Finished result processing in {(clock() - startTime):.3f}.")

	def _LoadVars(self):
		with open(self.VarIDFile, "r") as f:
			logger.info(f"Loading variables from file: {self.VarIDFile}")
			for line in f:
				line = line.strip()
				if line:
					id, r, p, g = map(int, line.split())
					self.Vars.append([id, r, p, g])

	def _LoadModel(self):
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
