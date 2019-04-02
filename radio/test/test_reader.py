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

def test_init_valid_input():
    input_backup = ReplaceStdIn("123\n45\nTO 1\n")
    reader = Reader()
    input_backup.cleanup()

    assert reader.recipient_address() == 123
    assert reader.caller_address() == 45

def test_init_bad_recipient():
    input_backup = ReplaceStdIn("abc\n45\nTO 1\n")
    reader = Reader()
    input_backup.cleanup()

    assert not reader.is_valid()

def test_init_bad_caller():
    input_backup = ReplaceStdIn("123\nde\nTO 1\n")
    reader = Reader()
    input_backup.cleanup()

    assert not reader.is_valid()

def test_init_bad_stream():
    input_backup = ReplaceStdIn("abc\n45\nTO 1\n")
    sys.stdin.close()
    reader = Reader()
    input_backup.cleanup()

    assert not reader.is_valid()

def test_init_short_stream():
    input_backup = ReplaceStdIn("123\n")
    reader = Reader()
    input_backup.cleanup()

    assert not reader.is_valid()

def test_next_character_empty_stream():
    input_backup = ReplaceStdIn("123\n45\n")
    reader = Reader()
    next_char = reader._next_character()
    input_backup.cleanup()

    assert next_char is None

def test_next_character_single_character_left():
    input_backup = ReplaceStdIn("123\n45\nT")
    reader = Reader()
    next_char = reader._next_character()
    input_backup.cleanup()

    assert next_char == "T"

def test_next_character_many_characters_left():
    input_backup = ReplaceStdIn("123\n45\nTO 1\nTO 1\n TO 1")
    reader = Reader()
    next_char = reader._next_character()
    input_backup.cleanup()

    assert next_char == "T"