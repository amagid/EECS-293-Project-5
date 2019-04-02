# The ConnectionState class represents the current state of the connection.
# CONNECTED state is static, while FAILURE is a method generating a failed
# state with the given reason.

class ConnectionState:
    pass
    # CONNECTED = ""
    # FAILURE = ""
    # FAILURE_INVALID_RECIPIENT = " invalid recipient"
    # FAILURE_RECIPIENT_NOT_ME = " recipient not me"
    # FAILURE_INVALID_CALLER = " invalid caller"

    # TO_STRING():
    #     initialize output to empty string
    #     if self is ConnectionState.CONNECTED, append "true" to output
    #     else append "false" to output
    #     append enum instance value to output

