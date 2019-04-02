import pytest
import sys
from io import StringIO
from radio.reader import Reader

class ReplaceStdIn:
    def __init__(self, input):
        self._STDIN = sys.stdin
        sys.stdin = StringIO(input)

    def cleanup(self):
        sys.stdin = self._STDIN

def test_init():
    input_backup = ReplaceStdIn("123\n45\n")

    reader = Reader()

    input_backup.cleanup()

    assert reader.recipient_address() == 123
    assert reader.caller_address() == 45
