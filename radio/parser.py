# The Parser class is responsible for taking the proper-type whole messages
# from the Reader and parsing them into valid-type messages. The scope of the
# Parser is limited to a single message, so it does not verify message order or
# placement in stream.

class Parser:
    pass
    # # INIT method initializes a Reader to be stored internally
    # INIT():
    #     initialize a Reader and store it in self._reader
    #     initialize self._leftovers to None

    
    # # Returns my actual recipient address (SETUP METHOD)
    # RECIPIENT_ADDRESS():
    #     return self._reader.RECIPIENT_ADDRESS()


    # # Returns the actual caller address (DEBUG METHOD)
    # CALLER_ADDRESS():
    #     return self._reader.CALLER_ADDRESS()

    
    # # Returns the next whole message as an instance of the Message class
    # NEXT_MESSAGE():
    #     store self._reader.NEXT_MESSAGE in message variable
    #     store _EXTRACT_COMMAND_AND_VALUE(message) in command, value
    #     generate Message instance from command and value inputs
    #     return generated Message instance

    
    # # Reads a single raw message string and returns the command and value as best it can
    # _EXTRACT_COMMAND_AND_VALUE(message):
    #     split message on space delimiter and store in raw_command and raw_value
    #     store Command.CLOSEST_MATCH(raw_command) in command
    #     store _CLEAN_VALUE(raw_value) in value, leftovers
    #     store leftovers in _leftovers
    #     return command, value

    
    # # Parses a potential value, separates and returns the first "good" value it sees as well as the leftovers
    # _CLEAN_VALUE(raw_value):
    #     iterate through string until digits found
    #     store read digits as a number in value
    #     store remainder of message to right of value in leftovers
    #     return value, leftovers

