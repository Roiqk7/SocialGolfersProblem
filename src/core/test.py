from main import Main
from pathlib import Path
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

def checkSolution(path: Path):
        # TODO: Implement
        pass

class SocialGolfersProblem(unittest.TestCase):
        @timeout(1)
        def testSmallSolvable(self):
                args = ["main", "--N", "8", "--G", "4", "--S", "2", "--R", "5", "--T", "1"]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, 0)

        @timeout(1)
        def testSmallUnsolvable(self):
                args = ["main", "--N", "8", "--G", "2", "--S", "4", "--R", "5", "--T", "1"]
                with patch("sys.argv", args):
                        code = Main()
                self.assertEqual(code, 1)

if __name__ == '__main__':
        unittest.main()
