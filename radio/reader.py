# The Reader class is responsible for reading inputs from the input stream and
# ensuring they are of the correct type and exist before passing them to the
# Parser.

class Reader:
    pass
    # Initializer connects the Reader to standard input
    # INIT():
    #     store input stream in self._input
    #     store caller address in self._caller_address
    #     store recipient address in self._recipient_address


    # # Return the actual recipient address (SETUP METHOD)
    # RECIPIENT_ADDRESS():
    #     return self._recipient_address


    # # Return the actual caller address (DEBUG METHOD)
    # CALLER_ADDRESS():
    #     return self._caller_address

    
    # # NEXT_MESSAGE is responsible for retrieving the next whole message
    # # Returns None if we are at the end of the stream
    # # Makes no promises about the formatting of a message - simply ensures the message is of the correct data type and exists
    # NEXT_MESSAGE():
    #     initialize string output to empty string
    #     if _NEXT_CHARACTER() is not a newline:
    #         append _NEXT_CHARACTER() to output string

    #     return output string


    # # _NEXT_CHARACTER is an internal method responsible for reading the next character from the input stream
    # # Returns None if there is no next character
    # _NEXT_CHARACTER():
    #     if _INPUT_STREAM_VALID():
    #         return next character from input stream
    #     else:
    #         return None


    # # _INPUT_STREAM_VALID detecs whether the input stream is still valid
    # _INPUT_STREAM_VALID():
    #     return True if input stream is still open and has more characters in it

