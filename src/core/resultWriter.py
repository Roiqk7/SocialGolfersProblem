from globals import *
import os

class ResultWriter:
	def __init__(self, N: int, G: int, S: int, R: int, T: int, content: str = None):
		if content == None:
			return
		self.N = N
		self.G = G
		self.S = S
		self.R = R
		self.T = T
		self.OutputFile = PROCESSED_RESULT_PATH
		self.Content = content
		self.Write()

	def Write(self, toStdout: bool = True):
		"""
		Writes the stored content to the file and optionally to standard output.

		This method handles the creation of directories if they don't exist and
		reports errors to standard error if writing fails.

		Args:
		toStdout (bool): If True, prints the content to the console (stdout).
				      Defaults to True.

		Throws:
		IOError: If the writing is interrupted, this exception is raised.
		"""
		if toStdout:
			self._WritePrettyConsole()

		try:
			# Ensure the directory for the file exists. (which it should)
			directory = os.path.dirname(self.OutputFile)
			if directory:
				os.makedirs(directory, exist_ok=True)

			logger.info(f"Writing result to file: {self.OutputFile}")
			with open(self.OutputFile, "w", encoding="utf-8") as f:
				f.write(self.Content)
			return True

		except Exception as e:
			logger.error(f"Error writing to file: {e}")
			raise IOError(f"Error writing to file: {e}")

	def _DetermineGroupWidths(self, roundsData: list[str]) -> list[int]:
		"""
		Searches all rounds to find the max display width for each group column.

		Args:
		roundsData (list[str]): List of raw round strings (e.g., 'P1,P2;P3,P4').

		Returns:
		list[int]: A list where each index `i` holds the max width for group `i`.
		"""
		if not roundsData:
			return []

		parsedRounds = [
			[group.replace(',', ', ') for group in roundStr.split(';')]
			for roundStr in roundsData
		]

		if not parsedRounds:
			return []

		groupCount = self.G if hasattr(self, 'G') and self.G > 0 else len(parsedRounds[0])
		maxWidths = [0] * groupCount

		for roundGroups in parsedRounds:
			for i, groupStr in enumerate(roundGroups):
				if i < groupCount:
					maxWidths[i] = max(maxWidths[i], len(groupStr))

		return maxWidths

	def _GetSeparatorLine(self, maxWidths: list[int], prefixWidth: int) -> str:
		"""
		Constructs the `---+---` separator line aligned to the table.

		Args:
		maxWidths (list[int]): The list of max widths for each group column.
		prefixWidth (int): The fixed width of the 'Round XX: ' label.

		Returns:
		str: The formatted separator line with correct left padding.
		"""
		separatorLine = ""
		for i, width in enumerate(maxWidths):
			separatorLine += "-" * width
			if i < len(maxWidths) - 1:
				separatorLine += "-+-"

		return " " * prefixWidth + separatorLine

	def _WritePrettyConsole(self):
		"""
		Prints the formatted schedule, handling 2-digit round alignment and
		centering the title over the table body.
		"""
		titleText = "S C H E D U L E"

		if self.Content == "UNSAT":
			self._WriteUnsat(titleText)
			return

		rounds = self.Content.split("\n")
		if not rounds or not rounds[0]:
			return

		maxWidths = self._DetermineGroupWidths(rounds)
		prefixWidth = len("Round XX: ")

		separatorLine = self._GetSeparatorLine(maxWidths, prefixWidth)

		groupWidth = sum(maxWidths)
		separatorWidth = (len(maxWidths) - 1) * 3
		tableBodyWidth = groupWidth + separatorWidth

		print()
		print(" " * prefixWidth + titleText.center(tableBodyWidth))
		print(separatorLine)

		for i, roundStr in enumerate(rounds):
			self._WritePrettyRound(roundStr, i, maxWidths, prefixWidth)
			print(separatorLine)

	def _WritePrettyRound(self, roundStr: str, indx: int, maxWidths: list[int], prefixWidth: int):
		"""
		Prints a single, formatted round line with fixed label width.

		Args:
		roundStr (str): The raw string for one round.
		indx (int): The round number.
		maxWidths (list[int]): The list of max widths for column alignment.
		prefixWidth (int): The fixed total length for the label.
		"""
		groups = roundStr.split(';')
		formattedGroups = []

		for i, group in enumerate(groups):
			if i < len(maxWidths):
				displayGroup = group.replace(',', ', ')
				width = maxWidths[i]
				formattedGroups.append(displayGroup.ljust(width))
			else:
				formattedGroups.append(group.replace(',', ', '))

		outputLine = " | ".join(formattedGroups)

		label = f"Round {indx}: "
		print(f"{label.ljust(prefixWidth)}{outputLine}")

	def _WriteUnsat(self, title: str, toStdout: bool = True):
		logger.info(f"Result: UNSAT; Writing into output file: {self.OutputFile}")
		with open(self.OutputFile, "w") as f:
			f.write("UNSAT")
		if toStdout:
			print()
			print("#-------------------------------------------------------------#")
			print("| There is no schedule which satisfies the given constraints. |")
			print("#-------------------------------------------------------------#")
			print()
