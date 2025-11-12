from globals import *
import os

class ResultWriter:
	def __init__(self, content: str = None):
		if content == None:
			return
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
			print(self.Content)

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
