import pytest
import sys
from radio.parser import Parser
from radio.test.utils import ReplaceStdIn
from radio.command import Command
from radio.message import Message

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

PARSE_CLEAN_VALUE_TEST_CASES = [
    ("", None),
    ("1", 1),
    ("ABC", None),
    (None, None)
]
@pytest.mark.parametrize(
    'test_case', PARSE_CLEAN_VALUE_TEST_CASES
)
def test_next_message_invalid(test_case):
    raw_value = test_case[0]
    expected_value = test_case[1]
    parser = Parser()

    result = parser._parse_clean_value_string(raw_value)

    assert result == expected_value

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
    ("", Command.INVALID, None),
    ("1", Command.INVALID, 1),
    ("TO 1", Command.TO, 1),
    ("TO1", Command.TO, 1),
    ("TO1)", Command.TO, 1),
    ("RE5P", Command.REP, 5),
    ("RFPG4", Command.REP, 4),
    ("TO8TO8TO8", Command.TO, 8)
]
@pytest.mark.parametrize(
    'test_case', EXTRACT_COMMAND_AND_VALUE_TEST_CASES
)
def test_extract_command_and_value(test_case):
    parser = Parser()
    message = test_case[0]
    expected_command = test_case[1]
    expected_value = test_case[2]

    command, value = parser._extract_command_and_value(message)

    assert command is expected_command
    assert value == expected_value

NEXT_MESSAGE_VALID_TEST_CASES = [
    ("TO 1", Command.TO, 1),
    ("TO1", Command.TO, 1),
    ("TO1)", Command.TO, 1),
    ("RE5P", Command.REP, 5),
    ("RFPG4", Command.REP, 4),
    ("TO8TO8TO8", Command.TO, 8)
]
@pytest.mark.parametrize(
    'test_case', NEXT_MESSAGE_VALID_TEST_CASES
)
def test_next_message_valid(test_case):
    message = test_case[0]
    expected_command = test_case[1]
    expected_value = test_case[2]
    input_backup = ReplaceStdIn("123\n45\n" + message + '\n')
    parser = Parser()

    parsed_message = parser.next_message()

    input_backup.cleanup()

    assert parsed_message.command() is expected_command
    assert parsed_message.value() is expected_value

NEXT_MESSAGE_INVALID_TEST_CASES = [
    "",
    "1", 
    "1TO", 
    "REP"
]
@pytest.mark.parametrize(
    'test_case', NEXT_MESSAGE_INVALID_TEST_CASES
)
def test_next_message_invalid(test_case):
    message = test_case
    input_backup = ReplaceStdIn("123\n45\n" + message + '\n')
    parser = Parser()

    parsed_message = parser.next_message()

    input_backup.cleanup()

    assert parsed_message is Message.INVALID