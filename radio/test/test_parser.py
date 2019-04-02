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

def test_clean_value_only_valid_value():
    parser = Parser()
    value, leftovers = parser._clean_value("123")

    assert value == 123
    assert leftovers == ''

def test_clean_value_valid_value_right_padded():
    parser = Parser()
    value, leftovers = parser._clean_value("123abc")

    assert value == 123
    assert leftovers == 'abc'

def test_clean_value_valid_value_left_padded():
    parser = Parser()
    value, leftovers = parser._clean_value("abc123")

    assert value == 123
    assert leftovers == ''

def test_clean_value_terminates_on_first_non_digit_after_digit_found():
    parser = Parser()
    value, leftovers = parser._clean_value("abc1234a56abc")

    assert value == 1234
    assert leftovers == 'a56abc'