from collections import defaultdict
from main import Main
from globals import *
from pathlib import Path
from unittest.mock import patch
import signal
import unittest
import warnings

def timeout(seconds=1):
        def decorator(func):
                def _handleTimeout(signum, frame):
                        raise TimeoutError(f"Test exceeded {seconds} seconds")

                def wrapper(*args, **kwargs):
                        signal.signal(signal.SIGALRM, _handleTimeout)
                        # start alarm
                        signal.alarm(seconds)
                        try:
                                # Actually runs the code
                                return func(*args, **kwargs)
                        finally:
                                # cancel alarm
                                signal.alarm(0)
                return wrapper
        return decorator

class SolutionChecker():
        def __init__(self):
                self.Solution = []

        def CheckSolution(self, solutionPath: Path, N: int, R: int, G: int, S: int, T: int) -> bool:
                """
                Checks if a solution is valid.

                Performs all the possible enumeration checks. Also checks if all the constraints
                are satisfied. The method uses assert for all of this.

                Args:
                solutionPath (Path): Path to the solution.
                N (int): Number of players.
                R (int): Number of rounds.
                G (int): Number of groups.
                S (int): Size of each group.
                T (int): Number of times a pair can meet.

                Returns:
                bool: If the solution is valid.
                """

                warnings.warn(
                        "SolutionChecker.CheckSolution is deprecated due to changed format in the main application's stdout return format.",
                        DeprecationWarning,
                        stacklevel=2
                )

                # 1. Load the solution
                self._LoadSolution(solutionPath)

                # UNSAT trivial case
                if self.Solution == []:
                        return True

                # 2. Check if there is correct number of rounds
                # 3. Check if there is correct number of groups in all rounds
                # 4. Check if all groups have correct size
                # 5. Check if the total player count is correct
                # 6. Check that all pairs meet the correct amount of times
                try:
                        uniquePlayersTotal = set()
                        pairMeets = defaultdict(lambda: defaultdict(int))
                        assert len(self.Solution) == R, f"Expected {R} rounds, but found {len(self.Solution)}."
                        for roundIndex, round in enumerate(self.Solution):
                                assert len(round) == G, f"Expected {G} groups, but found {len(round)} groups in round {roundIndex}."
                                playersInRound = set()
                                for group in round:
                                        assert len(group) == S, f"Expected {S} groups, but found group with size {len(group)} in round {roundIndex}."
                                        assert len(set(group)) == S, f"Group {group} in Round {roundIndex} contains duplicate players."
                                        for player in group:
                                                playersInRound.add(player)
                                                uniquePlayersTotal.add(player)
                                        # Iterate over all pairs in the group
                                        for i in range(S):
                                                for j in range(i + 1, S):
                                                        p1 = group[i]
                                                        p2 = group[j]
                                                        if p1 > p2:
                                                                p1, p2 = p2, p1
                                                        pairMeets[p1][p2] += 1
                                                        count = pairMeets[p1][p2]
                                                        assert count <= T, f"Expected the players {p1} and {p2} to shared the same group at most {T} times but it was {count}"
                                assert len(playersInRound) == N, f"Expected {N} players in round {roundIndex}, but found {len(playersInRound)}."
                        assert len(uniquePlayersTotal) == N, f"Expected {N} players, but found {len(uniquePlayersTotal)}."
                except Exception as e:
                        logger.error(f"Solution check failed: {e}")
                        return False
                return True

        def _LoadSolution(self, solutionPath: Path):
                """
                Loads a solution from the given path.

                If the solution is "UNSAT", sets self.Solution to []. Otherwise it fills
                the self.Solution such that self.Solution[i] contains information about
                one round. self.Solution[i][j] is a given group in the round. The group
                contains the player IDs.

                Args:
                solutionPath (Path): Path to the solution.

                Raises:
                IOError: If the reading of the solution fails.
                """
                try:
                        with open(solutionPath, "r") as f:
                                for line in f:
                                        if line == "UNSAT":
                                                self.Solution = []
                                                return
                                        groupsStr = line.strip().split(";")
                                        round = []
                                        for group in groupsStr:
                                                round.append(list(map(int, group.split(","))))
                                        self.Solution.append(round)
                except Exception as e:
                        logger.error(e)
                        raise IOError(f"Could not load solution: {e}")


class SGPTests(unittest.TestCase):
        def setUp(self):
                self.SolutionChecker = SolutionChecker()
                self.SOLVABLE_EXIT_CODE = 0
                self.UNSAT_EXIT_CODE = 1
                self.ERROR_EXIT_CODE = 2
                self.V = 0

        @timeout(1)
        def testTrivialSolvable(self):
                N, G, S, R, T = 2, 1, 2, 1, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.SOLVABLE_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testTrivialSolvable2(self):
                N, G, S, R, T = 2, 1, 2, 2, 2
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.SOLVABLE_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testTrivialSolvable3(self):
                N, G, S, R, T = 2, 1, 2, 3, 3
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.SOLVABLE_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testTrivialUnsolvable(self):
                N, G, S, R, T = 2, 1, 2, 2, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T),
                        "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.UNSAT_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testTrivialUnsolvable2(self):
                N, G, S, R, T = 2, 1, 2, 4, 3
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.UNSAT_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testSmallSolvable(self):
                N, G, S, R, T = 4, 4, 1, 5, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.SOLVABLE_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testSmallUnsolvable(self):
                N, G, S, R, T = 4, 1, 4, 2, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.UNSAT_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testMediumSolvable(self):
                N, G, S, R, T = 8, 4, 2, 5, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.SOLVABLE_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testMediumUnsolvable(self):
                N, G, S, R, T = 8, 2, 4, 5, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.UNSAT_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(15)
        def testLargeSolvable(self):
                N, G, S, R, T = 12, 4, 3, 3, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.SOLVABLE_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(5)
        def testLargeUnsolvable(self):
                N, G, S, R, T = 12, 3, 4, 4, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.UNSAT_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(20)
        def testVeryLargeSolvable(self):
                N, G, S, R, T = 16, 4, 4, 5, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, self.SOLVABLE_EXIT_CODE)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

if __name__ == '__main__':
        unittest.main()
