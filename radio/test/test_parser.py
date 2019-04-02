import pytest
import sys
from radio.parser import Parser
from radio.test.utils import ReplaceStdIn
from radio.command import Command

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

def test_first_digit_index_only_digit():
    parser = Parser()
    index = parser._first_digit_index("1")

    assert index == 0

def test_first_digit_index_empty_input():
    parser = Parser()
    index = parser._first_digit_index("")

    assert index == 0

def test_first_digit_index_no_digits():
    parser = Parser()
    index = parser._first_digit_index("abc")

    assert index == 3

def test_first_digit_index_left_padded():
    parser = Parser()
    index = parser._first_digit_index("abcd1")

    assert index == 4


EXTRACT_COMMAND_AND_VALUE_TEST_CASES = [
    ("", Command.INVALID, None)
]
@pytest.mark.parametrize(
    'test_case', EXTRACT_COMMAND_AND_VALUE_TEST_CASES
)
def test_extract_command_and_value_empty_input(test_case):
    parser = Parser()
    message = test_case[0]
    expected_command = test_case[1]
    expected_value = test_case[2]

    command, value = parser._extract_command_and_value(message)

    assert command is expected_command
    assert value == expected_value

    