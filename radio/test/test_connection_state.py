import pytest
from radio.connection_state import ConnectionState

TEST_STRINGS = [
    (ConnectionState.CONNECTED, "true"),
    (ConnectionState.FAILURE, "false generic error"),
    (ConnectionState.FAILURE_INVALID_RECIPIENT, "false" + ConnectionState.FAILURE_INVALID_RECIPIENT.value),
]
@pytest.mark.parametrize(
    'test_string_case', TEST_STRINGS
)
def test_str(test_string_case):
    state = test_string_case[0]
    expected = test_string_case[1]

    result = str(state)

    assert result == expected