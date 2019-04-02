import pytest
import sys
from radio.parser import Parser
from radio.test.utils import ReplaceStdIn

def test_init_assigns_properties():
    input_backup = ReplaceStdIn("123\n45\nTO 1\n")
    parser = Parser()
    input_backup.cleanup()

    assert parser._reader.is_valid()
    assert parser._leftovers is None

def test_address_getters():
    input_backup = ReplaceStdIn("123\n45\nTO 1\n")
    parser = Parser()
    input_backup.cleanup()

    assert parser.recipient_address() == 123
    assert parser.caller_address() == 45