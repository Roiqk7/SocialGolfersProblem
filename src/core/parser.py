from globals import *
import argparse
import logging
import os

def ParseArgs():
	try:
		logger.debug("Parsing arguments...")
		parser = argparse.ArgumentParser(description="Social Golfers SAT Solver")
		parser.add_argument("--N", type=int, default=32, help="Number of golfers (default: 32)")
		parser.add_argument("--G", type=int, default=8, help="Number of groups per round (default: 8)")
		parser.add_argument("--S", type=int, default=4, help="Size of each group (default: 4)")
		parser.add_argument("--R", type=int, default=10, help="Number of rounds (default: 10)")
		parser.add_argument("--T", type=int, default=1, help="Max times a pair can meet (default: 1)")
		parser.add_argument("--I", type=str, default=DEFAULT_CNF_FILE_PATH, help=f"Input file in DIMACS CNF format (default: {DEFAULT_CNF_FILE_PATH}")
		parser.add_argument("--O", type=str, default=DEFAULT_SOLVER_OUTPUT_FILE_PATH, help=f"Output file of the SAT solver (default: {DEFAULT_SOLVER_OUTPUT_FILE_PATH}")
		parser.add_argument("--V", type=int, default=1, choices=[0, 1, 2], help="Verbosity level for logging (default: 0)")
		parser.add_argument("--test", action="store_true", default=False, help="If present, runs the test suite.")
		args = parser.parse_args()
		CheckArgs(args)
		SetVervosity(args.V)
		logger.info(f"Args: {args}")
		logger.debug("Finished parsing arguments.")
		return args
	except Exception as e:
		logger.error(e)
		raise ValueError(f"Could not parse arguments: {e}")

def CheckArgs(args):
	# Consistency check: N = G * S
	if args.N != args.G * args.S:
		raise ValueError(
			f"Inconsistent parameters: N must equal G * S.\n"
			f"Got N={args.N}, G={args.G}, S={args.S} (G*S={args.G * args.S})."
		)

	# Positivity check
	for name, val in [("N", args.N), ("G", args.G), ("S", args.S), ("R", args.R), ("T", args.T)]:
		if val <= 0:
			raise ValueError(f"Parameter {name} must be a positive integer, got {val}.")

	# Verbosity check
	if args.V not in [0, 1, 2]:
		logger.warn(f"Verbosity level {args.V} is not supported. Resetting to default: 0.")
		args.V = 0

	# Check if files exist
	if not os.path.exists(args.I):
		message = f"Input file {args.I} does not exist."
		logger.error(f"Input file {args.I} does not exist.")
		raise ValueError(message)

	if not os.path.exists(args.O):
		message = f"Output file {args.O} does not exist."
		logger.error(message)
		raise ValueError(message)

def SetVervosity(V: int):
	if V == 0:
		logLevel = logging.WARNING
	elif V == 1:
		logLevel = logging.INFO
	elif V == 2:
		logLevel = logging.DEBUG
	else:
		logLevel = logging.INFO
	logger.setLevel(logLevel)
	logger.debug(f"Verbosity level is set to {V} ({logging.getLevelName(logLevel)}).")
