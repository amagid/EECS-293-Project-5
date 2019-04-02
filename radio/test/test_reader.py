import pytest
import sys
from radio.reader import Reader
from radio.test.utils import ReplaceStdIn

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

def test_next_character_twice_many_characters_left():
    input_backup = ReplaceStdIn("123\n45\nTO 1\nTO 1\n TO 1")
    reader = Reader()
    next_char = reader._next_character()
    next_char2 = reader._next_character()
    input_backup.cleanup()

    assert next_char == "T"
    assert next_char2 == "O"

def test_next_message_many_messages_left():
    input_backup = ReplaceStdIn("123\n45\nTO 1\nREP 1\n REP 1")
    reader = Reader()
    next_message = reader.next_message()
    input_backup.cleanup()

    assert next_message == "TO 1"

def test_next_message_twice_many_messages_left():
    input_backup = ReplaceStdIn("123\n45\nTO 1\nREP 1\n REP 1")
    reader = Reader()
    next_message = reader.next_message()
    next_message2 = reader.next_message()
    input_backup.cleanup()

    assert next_message == "TO 1"
    assert next_message2 == "REP 1"

def test_next_message_no_messages_left():
    input_backup = ReplaceStdIn("123\n45\n")
    reader = Reader()
    next_message = reader.next_message()
    input_backup.cleanup()

    assert next_message is None

def test_next_message_empty_message_next():
    input_backup = ReplaceStdIn("123\n45\n\n\nTO 1\n")
    reader = Reader()
    next_message = reader.next_message()
    input_backup.cleanup()

    assert next_message is None