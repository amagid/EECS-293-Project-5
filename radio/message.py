# The Message class represents a cleaned and parsed single message, containing
# a command and a value.

from radio.command import Command

class Message:
    # The static INVALID Message instance is used for any message that cannot be parsed reliably
    INVALID = None

    # The INIT method takes a Command instance and a numerical value and stores them
    def __init__(self, command, value):
        self._command = command
        self._value = value


    # Builds a new Message instance. Returns the INVALID instance if the given inputs are invalid
    @staticmethod
    def build(command, value):
        if isinstance(command, Command) and command is not Command.INVALID and value is not None:
            return Message(command, value)
        else:
            return Message.INVALID


    # Retrieve the stored Command
    def command(self):
        return self._command


    # Retrive the stored Value
    def value(self):
        return self._value


    # Check whether or not this Message is valid
    def is_valid(self):
        return self != Message.INVALID

# Initialize INVALID message
Message.INVALID = Message(None, None)