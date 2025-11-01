from collections import defaultdict
from main import Main
from globals import *
from pathlib import Path
from typing import Set
from unittest.mock import patch
import signal
import unittest

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
                return True

        def _LoadSolution(self, solutionPath: Path):
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


class SocialGolfersProblem(unittest.TestCase):
        def setUp(self):
                self.SolutionChecker = SolutionChecker()
                self.V = 0

        @timeout(1)
        def testTrivialSolvable(self):
                N, G, S, R, T = 10, 1, 10, 1, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V",
                        str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, 0)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testMiniSolvable(self):
                N, G, S, R, T = 4, 4, 1, 5, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, 0)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testMiniUnsolvable(self):
                N, G, S, R, T = 4, 1, 4, 2, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, 1)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testSmallSolvable(self):
                N, G, S, R, T = 8, 4, 2, 5, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, 0)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

        @timeout(1)
        def testSmallUnsolvable(self):
                N, G, S, R, T = 8, 2, 4, 5, 1
                args = ["main", "--N", str(N), "--G", str(G), "--S", str(S), "--R", str(R), "--T", str(T), "--V", str(self.V)]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, 1)
                self.assertTrue(self.SolutionChecker.CheckSolution(PROCESSED_RESULT_PATH, N, R, G, S, T))

if __name__ == '__main__':
        unittest.main()
