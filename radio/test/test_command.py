import pytest
from radio.command import Command

# Helper Methods

def _generate_score_dictionary(to_score, rep_score, thisis_score):
    return {
        "TO": to_score,
        "REP": rep_score,
        "THISIS": thisis_score
    }

# Tests

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


COMMAND_WITH_HIGHEST_SCORE_TEST_CASES = [
    (_generate_score_dictionary(0, 0, 0), Command.INVALID),
    (_generate_score_dictionary(-1, -2, -3), Command.INVALID),
    (_generate_score_dictionary(1, 0, 0), Command.TO),
    (_generate_score_dictionary(1, 2, 1), Command.REP),
    (_generate_score_dictionary(1, 2, 3), Command.THISIS),
    (_generate_score_dictionary(3, 2, 3), Command.TO)
]
@pytest.mark.parametrize(
    'test_case', COMMAND_WITH_HIGHEST_SCORE_TEST_CASES
)
def test_letters_in_common(test_case):
    command = Command.INVALID
    score_dictionary = test_case[0]
    expected = test_case[1]

    result = command._command_with_highest_score(score_dictionary)

    assert result == expected