from globals import DEFAULT_CNF_FILE_PATH
import os
from pathlib import Path

class ProblemInstance:
	def __init__(self, N: int, G: int, S: int, R: int, T: int):
		self._Init(N, G, S, R, T)
		self._EncodeClauses()

	def _Init(self, N: int, G: int, S: int, R: int, T: int, InputFile: Path = None):
		self.N = N
		self.G = G
		self.S = S
		self.R = R
		self.T = T
		self.VariableNumber = 0
		self.VlauseNumber = 0
		if InputFile is None:
			self.OutputFile = DEFAULT_CNF_FILE_PATH
		else:
			self.OutputFile = InputFile

	def _EncodeClauses(self):
		self._EncodeOnePlayerPerGroup()

	def _GetVarID(self, r, p, g) -> int:
		return r * (self.N * self.G) + p * self.G + g + 1

	def _GetClause(self, arr: list[int]) -> str:
		return " ".join(str(x) for x in arr) + " 0\n"

	def _WriteClause(self, arr: list[int]) -> None:
		with open(self.OutputFile, "a") as f:
			f.write(self._GetClause(arr))

	def _EncodeOnePlayerPerGroup(self):
		# TODO: Test that it works
		for r in range(self.R):
			for p in range(self.N):
				# at least one group
				clause = [self._GetVarID(r, p, g) for g in range(self.G)]
				self._WriteClause(clause)

				# at most one group
				for g1 in range(self.G):
					for g2 in range(g1 + 1, self.G):
						self._WriteClause(
							[-self._GetVarID(r, p, g1), -self._GetVarID(r, p, g2)])
