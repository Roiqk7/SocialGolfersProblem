import coloredlogs
import logging
from pathlib import Path

DEFAULT_CNF_FILE_PATH = Path("data", "in", "input.cnf").as_posix()
DEFAULT_SOLVER_OUTPUT_FILE_PATH = Path("data", "out", "result.txt").as_posix()
DEFAULT_SOLVER_EXECUTABLE_PATH = Path("glucose", "simp", "glucose").as_posix()

logger = logging.getLogger("SGP")
coloredlogs.install(
	level="DEBUG",
	fmt="[%(levelname)s][%(name)s][%(asctime)s]: %(message)s",
	datefmt="%H:%M:%S.%f",
	logger=logger)
