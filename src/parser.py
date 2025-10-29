import argparse

def ParseArgs():
	parser = argparse.ArgumentParser(description="Social Golfers SAT Solver")
	parser.add_argument("--N", type=int, default=32, help="Number of golfers (default: 32)")
	parser.add_argument("--G", type=int, default=8, help="Number of groups per round (default: 8)")
	parser.add_argument("--S", type=int, default=4, help="Size of each group (default: 4)")
	parser.add_argument("--R", type=int, default=10, help="Number of rounds (default: 10)")
	parser.add_argument("--T", type=int, default=1, help="Max times a pair can meet (default: 1)")
	args = parser.parse_args()
	CheckArgs(args)
	return args

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
