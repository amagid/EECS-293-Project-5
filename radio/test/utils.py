import sys
from io import StringIO

class ReplaceStdIn:
    def __init__(self, input):
        self._STDIN = sys.stdin
        sys.stdin = StringIO(input)

    def cleanup(self):
        sys.stdin = self._STDIN