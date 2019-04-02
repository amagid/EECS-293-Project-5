# The Radio class is the master class of the program. It initializes an
# internally stored Parser and uses it to read valid, sanitized Messages from
# the input stream. It is responsible only for handling high-level protocol
# errors, and expects that all received Messages will be correctly formatted
# and exist, or otherwise be marked as INVALID.

from radio.parser import Parser
from radio.command import Command
from radio.message import Message
from radio.connection_state import ConnectionState

class Radio:
    # Controls whether or not exceptions are returned
    DEBUG = False

    # INIT initializes this Radio with an internal Parser
    def __init__(self):
        self._parser = Parser()
        self._to_address = None
        self._from_address = None 
        self._command_parsers = {
            Command.TO: self._PARSE_TO,
            Command.REP: self._PARSE_LONE_REP,
            Command.THISIS: self._PARSE_THISIS,
            Command.INVALID: self._PARSE_INVALID
        }

    
    # ATTEMPT_CONNECT is the main method. Reads messages one at a time and parses major message sections based on the received
    # message. Reading a message of a particular type kicks off parsing further for that type of message.
    # This method also swallows all exceptions when in production to ensure no raw errors ever make it back to the client.
    def attempt_connect(self):
        try:
            while self._parser.is_valid() and not CONNECTION_VALID():
                message = self._parser.next_message()
                self._command_parsers[message.command()](message)

            return str(self.connection_state())

        except Exception as e:
            if not DEBUG:
                return str(ConnectionState.FAILURE)
            else:
                raise e

    # connection_state checks if we can validly connect with the current status
    # and returns a ConnectionState appropriate to that conditional.
    def connection_state(self):
        state = None
        if CONNECTION_VALID():
            state = ConnectionState.CONNECTED
        else:
            state = _FAILED_CONNECTION_STATE()

        return state



    # # CONNECTION_VALID is a public method returning whether or not the connection is currently valid
    # CONNECTION_VALID():
    #     return True if self._to_address is equal to self._parser.RECIPIENT_ADDRESS() and self._from_address is a valid number equal to self._parser.CALLER_ADDRESS()


    # # _FAILED_CONNECTION_STATE returns the proper failure ConnectionState based on the current state information
    # _FAILED_CONNECTION_STATE():
    #     initialize error to _CHECK_RECIPIENT_ERROR()
    #     if error is None
    #         set error to _CHECK_CALLER_ERROR()
    #     if error is still None
    #         set error to ConnectionState.FAILURE

    #     return error


    # # _CHECK_RECIPIENT_ERROR returns the appropriate RECIPIENT_ERROR ConnectionState based on the current state information
    # # Returns None if there is no issue with the recipient information
    # _CHECK_RECIPIENT_ERROR():
    #     if self._to_address is invalid or missing, return ConnectionState.FAILURE_INVALID_RECIPIENT
    #     elif self._to_address is valid but not my address, return ConnectionState.FAILURE_RECIPIENT_NOT_ME
    #     else return None


    # # _CHECK_CALLER_ERROR returns the appropriate CALLER_ERROR ConnectionState based on the current state information
    # # Returns None if there is no issue with the caller information
    # _CHECK_CALLER_ERROR():
    #     if self._from_address is invalid or missing, return ConnectionState.FAILURE_INVALID_CALLER
    #     else return None

