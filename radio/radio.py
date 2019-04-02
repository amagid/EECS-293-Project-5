# The Radio class is the master class of the program. It initializes an
# internally stored Parser and uses it to read valid, sanitized Messages from
# the input stream. It is responsible only for handling high-level protocol
# errors, and expects that all received Messages will be correctly formatted
# and exist, or otherwise be marked as INVALID.

from radio.parser import Parser
from radio.command import Command
from radio.message import Message
from radio.connection_state import ConnectionState
from radio.radio_state import RadioState
class Radio:
    # Controls whether or not exceptions are returned
    DEBUG = True

    # INIT initializes this Radio with an internal Parser
    def __init__(self, stream = None):
        self._parser = Parser(stream)
        self._to_address = None
        self._from_address = None 
        self._command_parsers = {
            Command.TO: self._parse_to,
            Command.REP: self._parse_rep,
            Command.THISIS: self._parse_thisis,
            Command.INVALID: self._parse_invalid
        }
        self._state = RadioState(Command.INVALID, 0, '', 0)

    
    # ATTEMPT_CONNECT is the main method. Reads messages one at a time and parses major message sections based on the received
    # message. Reading a message of a particular type kicks off parsing further for that type of message.
    # This method also swallows all exceptions when in production to ensure no raw errors ever make it back to the client.
    def attempt_connect(self):
        if not self.is_valid():
            return str(ConnectionState.FAILURE)

        try:
            while self.is_valid() and not self.connection_valid():
                message = self._parser.next_message()
                self._command_parsers[message.command()](message)
            return str(self.connection_state())

        except Exception as e:
            return str(ConnectionState.FAILURE)

    def _parse_to(self, message):
        if self._state.current_section is Command.THISIS:
            self._commit_state()
            self._reset_state()
        self._state.current_section = Command.TO
        self._state.repeats += 1
        self._state.partial_address = str(message.value())
        self._state.invalid_count = 0

    def _parse_rep(self, message):
        if self._state.current_section is Command.THISIS or self._state.current_section is Command.TO:
            self._state.partial_address += str(message.value())
            self._state.invalid_count = 0

    def _parse_thisis(self, message):
        if self._state.current_section is Command.TO:
            self._commit_state()
            self._reset_state()

        self._state.current_section = Command.THISIS
        self._state.repeats += 1
        self._state.partial_address = str(message.value())
        self._state.invalid_count = 0

    def _parse_invalid(self, message):
        self._commit_state()
        self._state.invalid_count += 1

    def _commit_state(self):
        if self._state.current_section is Command.TO:
            self._to_address = int(self._state.partial_address)
        elif self._state.current_section is Command.THISIS:
            self._from_address = int(self._state.partial_address)

    def _reset_state(self):
        self._state.current_section = Command.INVALID
        self._state.repeats = 0
        self._state.partial_address = ''
        self._state.invalid_count = 0

    # connection_state checks if we can validly connect with the current status
    # and returns a ConnectionState appropriate to that conditional.
    def connection_state(self):
        state = None
        if self.connection_valid():
            state = ConnectionState.CONNECTED
        else:
            state = self._failed_connection_state()

        return state



    # CONNECTION_VALID is a public method returning whether or not the connection is currently valid
    def connection_valid(self):
        return self._to_address == self._parser.recipient_address() and isinstance(self._parser.recipient_address(), int) and self._from_address == self._parser.caller_address() and isinstance(self._parser.caller_address(), int)


    # _FAILED_CONNECTION_STATE returns the proper failure ConnectionState based on the current state information
    def _failed_connection_state(self):
        return self._check_recipient_error() or self._check_caller_error() or None


    # _CHECK_RECIPIENT_ERROR returns the appropriate RECIPIENT_ERROR ConnectionState based on the current state information
    # Returns None if there is no issue with the recipient information
    def _check_recipient_error(self):
        if not self._to_address or not isinstance(self._to_address, int):
            return ConnectionState.FAILURE_INVALID_RECIPIENT
        elif isinstance(self._to_address, int) and self._to_address != self._parser.recipient_address():
            return ConnectionState.FAILURE_RECIPIENT_NOT_ME
        else:
            return None


    # _CHECK_CALLER_ERROR returns the appropriate CALLER_ERROR ConnectionState based on the current state information
    # Returns None if there is no issue with the caller information
    def _check_caller_error(self):
        if not self._from_address or not isinstance(self._from_address, int):
            return ConnectionState.FAILURE_INVALID_CALLER
        else:
            return None

    def is_valid(self):
        return self._state.invalid_count < 10 and self._parser.is_valid()

