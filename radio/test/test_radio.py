import pytest
import sys
from radio.radio import Radio
from radio.test.utils import ReplaceStdIn
from radio.command import Command
from radio.message import Message
from radio.connection_state import ConnectionState

INTEGRATION_TEST_CASES = [
    ("123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n", ConnectionState.CONNECTED),
    ("123\n45\nTO 1\nTO 1\nTO 1\nTO 1\nTO 1\nTO 1\nTO 1\nREP 2\nREP 3\nTHISIS 4\nREP 5\n", ConnectionState.CONNECTED),
    ("123\n45\nTO 1\nTO 1\nTO 1\nTO 1\nTO 1\nTO 1\nTO 1\nREP 2\nGARBLED\nREP 3\nTHISIS 4\nREP 5\n", ConnectionState.CONNECTED),
    ("123\n45\nGARBLED\nREP 2\nREP 3\nTHISIS 4\nREP 5\n", ConnectionState.FAILURE_INVALID_RECIPIENT),
    ("123\n45\nTO 1\nREP 2\nREP 3\nGARBLED\nREP 5\n", ConnectionState.FAILURE_RECIPIENT_NOT_ME),
    ("123\n45\nTO 1\nREP 2\nREP 3\nTHISIS \n", ConnectionState.FAILURE_INVALID_CALLER),
    ("", ConnectionState.FAILURE),
]
@pytest.mark.parametrize(
    'test_case', INTEGRATION_TEST_CASES
)
def test_extract_command_and_value(test_case):
    input = test_case[0]
    expected_connection_state_string = str(test_case[1])
    input_backup = ReplaceStdIn(input)
    
    radio = Radio(sys.stdin)
    connection_state_string = radio.attempt_connect()

    input_backup.cleanup()

    assert connection_state_string == expected_connection_state_string


def test_check_caller_error_no_error():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = None
    
    radio = Radio(sys.stdin)
    radio._from_address = 4
    
    result = radio._check_caller_error()

    input_backup.cleanup()

    assert result == expected


def test_check_is_valid_valid():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = True
    
    radio = Radio(sys.stdin)
    
    result = radio.is_valid()

    input_backup.cleanup()

    assert result == expected

    
def test_check_recipient_error_no_to_address():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = ConnectionState.FAILURE_INVALID_RECIPIENT
    
    radio = Radio(sys.stdin)
    radio._to_address = None
    radio._parser._reader._recipient_address = 4
    
    result = radio._check_recipient_error()

    input_backup.cleanup()

    assert result == expected
    
def test_failed_connection_state_valid_state():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = None
    
    radio = Radio(sys.stdin)
    radio._to_address = 4
    radio._parser._reader._recipient_address = 4
    radio._from_address = 3
    radio._parser._reader._caller_address = 3
    
    result = radio._failed_connection_state()

    input_backup.cleanup()

    assert result == expected
    
def test_connection_valid():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = True
    
    radio = Radio(sys.stdin)
    radio._to_address = 4
    radio._parser._reader._recipient_address = 4
    radio._from_address = 3
    radio._parser._reader._caller_address = 3
    
    result = radio.connection_valid()

    input_backup.cleanup()

    assert result == expected
    
def test_connection_state_recipient_not_me():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = ConnectionState.FAILURE_RECIPIENT_NOT_ME
    
    radio = Radio(sys.stdin)
    radio._to_address = 3
    radio._parser._reader._recipient_address = 4
    radio._from_address = 3
    radio._parser._reader._caller_address = 3
    
    result = radio.connection_state()

    input_backup.cleanup()

    assert result == expected
    
def test_reset_state():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    
    radio = Radio(sys.stdin)

    radio._reset_state()

    input_backup.cleanup()

    assert radio._state.current_section == Command.INVALID
    assert radio._state.repeats == 0
    assert radio._state.partial_address == ''
    assert radio._state.invalid_count == 0   

def test_commit_state_to():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    
    radio = Radio(sys.stdin)
    radio._state.partial_address = '123'
    expected = int(radio._state.partial_address)
    
    radio._state.current_section = Command.TO
    
    radio._commit_state()

    result = radio._to_address

    input_backup.cleanup()

    assert result == expected


def test_commit_state_thisis():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    
    radio = Radio(sys.stdin)
    radio._state.partial_address = '123'
    expected = int(radio._state.partial_address)
    
    radio._state.current_section = Command.TO
    
    radio._commit_state()

    result = radio._to_address

    input_backup.cleanup()

    assert result == expected

    
def test_parse_invalid():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = 6
    
    radio = Radio(sys.stdin)
    radio._state.invalid_count = 5
    
    radio._parse_invalid(Message.INVALID)

    result = radio._state.invalid_count

    input_backup.cleanup()

    assert result == expected
    
def test_parse_invalid():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = 0
    
    radio = Radio(sys.stdin)
    radio._state.invalid_count = 5
    radio._state.partial_address = '123'
    radio._state.current_section = Command.TO
    
    radio._parse_thisis(Message.build(Command.THISIS, 4))

    result = radio._state.invalid_count

    input_backup.cleanup()

    assert result == expected

def test_parse_rep():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = '1234'
    
    radio = Radio(sys.stdin)
    radio._state.invalid_count = 5
    radio._state.partial_address = '123'
    radio._state.current_section = Command.TO
    
    radio._parse_rep(Message.build(Command.REP, 4))

    result = radio._state.partial_address

    input_backup.cleanup()

    assert result == expected

def test_commit_state_to():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    
    radio = Radio(sys.stdin)
    radio._state.partial_address = '123'
    expected = int(radio._state.partial_address)
    
    radio._state.current_section = Command.THISIS
    
    radio._commit_state()

    result = radio._from_address

    input_backup.cleanup()

    assert result == expected

def test_attempt_connect_really_bad():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = str(ConnectionState.FAILURE)
    radio = Radio(sys.stdin)
    radio.connection_valid = None
    
    result = radio.attempt_connect()

    input_backup.cleanup()

    assert result == expected

def test_attempt_connect_really_bad_is_valid_gone():
    input = "123\n45\nTO 1\nREP 2\n REP 3\nTHISIS 4\nREP 5\n"
    input_backup = ReplaceStdIn(input)
    expected = str(ConnectionState.FAILURE)
    radio = Radio(sys.stdin)
    radio.is_valid = lambda:False
    
    result = radio.attempt_connect()

    input_backup.cleanup()

    assert result == expected