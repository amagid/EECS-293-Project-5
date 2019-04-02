import pytest
from radio.command import Command

LETTERS_IN_COMMON_TEST_CASES = [
    (Command.TO, "TO", 2),
    (Command.REP, "TO", 0),
    (Command.TO, "RTO", 2),
    (Command.TO, "OT", 2),
    (Command.THISIS, "THISISA", 6),
    (Command.INVALID, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0)
]
@pytest.mark.parametrize(
    'test_case', LETTERS_IN_COMMON_TEST_CASES
)
def test_letters_in_common(test_case):
    command = test_case[0]
    raw_command = test_case[1]
    expected = test_case[2]

    result = command._letters_in_common(raw_command)

    assert result == expected