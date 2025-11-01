import logging
from pathlib import Path

DEFAULT_CNF_FILE_PATH = Path("data", "in", "input.cnf").as_posix()
DEFAULT_TMP_CNF_FILE_PATH = Path("data", "in", "tmp.cnf").as_posix()
DEFAULT_SOLVER_OUTPUT_FILE_PATH = Path("data", "out", "solver.txt").as_posix()
DEFAULT_SOLVER_EXECUTABLE_PATH = Path("glucose", "simp", "glucose").as_posix()
VAR_ID_FILE_PATH = Path("data", "in", "varID.txt").as_posix()
PROCESSED_RESULT_PATH = Path("data", "out", "result.txt").as_posix()
TEST_FILE_PATH = Path("src", "core", "test.py").as_posix()

logger = logging.getLogger("SGP")

try:
	import coloredlogs
	coloredlogs.install(
		level=logging.INFO,
		fmt="[%(levelname)s][%(name)s][%(asctime)s]: %(message)s",
		datefmt="%H:%M:%S.%f",
		logger=logger)
except ModuleNotFoundError:
	logging.basicConfig(
		level=logging.INFO,
		format="[%(levelname)s][%(name)s][%(asctime)s]: %(message)s",
		datefmt="%H:%M:%S",
	)
