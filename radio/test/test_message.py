import pytest
from radio.message import Message
from radio.command import Command

def test_init_assigns_values():
    command = Command.TO
    value = 3
    message = Message(command, value)

    assert message.command() is command
    assert message.value() is value


BUILD_TEST_CASES = [
    (Command.TO, 3, False),
    (Command.TO, None, True),
    (None, 3, True),
    (5, 6, True),
    (Command.INVALID, 4, True),
    (Command.REP, 7, False)
]
@pytest.mark.parametrize(
    'test_case', BUILD_TEST_CASES
)
def test_build(test_case):
    command = test_case[0]
    value = test_case[1]
    expect_message_invalid = test_case[2]

    message = Message.build(command, value)

    assert (message is Message.INVALID) == expect_message_invalid

def test_is_valid_valid():
    message = Message.build(Command.TO, 3)

    assert message.is_valid()

def test_is_valid_invalid():
    message = Message.INVALID

    assert not message.is_valid()

