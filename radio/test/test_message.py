import pytest
from radio.message import Message
from radio.command import Command

def test_init_assigns_values():
    command = Command.TO
    value = 3
    message = Message(command, value)

    assert message.command() is command
    assert message.value() is value
