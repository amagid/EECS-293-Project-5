# The Reader class is responsible for reading inputs from the input stream and
# ensuring they are of the correct type and exist before passing them to the
# Parser.

import sys

LINE_FEED = '\n'

class Reader:
    # Init connects the Reader to standard input
    def __init__(self):
        # Try to read recipient and caller addresses.
        # If fails for any reason, invalidate the input stream
        try:
            self._input = sys.stdin
            self._recipient_address = int(self._input.readline())
            self._caller_address = int(self._input.readline())
        except:
            self._input = None

        # If addresses were not set for any reason, invalidate the input stream
        if not isinstance(self.recipient_address(), int) and not isinstance(self.caller_address(), int):
            self._input = None


    # Return the actual recipient address (SETUP METHOD)
    def recipient_address(self):
        return self._recipient_address


    # Return the actual caller address (DEBUG METHOD)
    def caller_address(self):
        return self._caller_address

    
    # NEXT_MESSAGE is responsible for retrieving the next whole message
    # Returns None if we are at the end of the stream
    # Makes no promises about the formatting of a message - simply ensures the message is of the correct data type and exists
    def next_message(self):
        output = ""
        next_char = self._next_character()
        while next_char is not None and next_char != LINE_FEED:
            output += next_char
            next_char = self._next_character()

        return output


    # _NEXT_CHARACTER is an internal method responsible for reading the next character from the input stream
    # Returns None if there is no next character
    def _next_character(self):
        if self._input_stream_valid():
            return self._input.read()
        else:
            return None


    # # _INPUT_STREAM_VALID detecs whether the input stream is still valid
    # _INPUT_STREAM_VALID():
    #     return True if input stream is still open and has more characters in it

