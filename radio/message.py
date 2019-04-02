# The Message class represents a cleaned and parsed single message, containing
# a command and a value.

class Message:
    pass
    # # The static INVALID Message instance is used for any message that cannot be parsed reliably
    # INVALID = Message(None, None)

    # # The INIT method takes a Command instance and a numerical value and stores them
    # INIT(command, value):
    #     store command in self._command
    #     store value in self._value


    # # Builds a new Message instance. Returns the INVALID instance if the given inputs are invalid
    # BUILD(command, value):
    #     if command or value is None, return the INVALID Message instance.
    #     else return a newly initialized Message


    # # Retrieve the stored Command
    # COMMAND():
    #     return self._command


    # # Retrive the stored Value
    # VALUE():
    #     return self._value


    # # Check whether or not this Message is valid
    # IS_VALID():
    #     return self != INVALID Message instance

