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