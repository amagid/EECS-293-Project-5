# The ConnectionState class represents the current state of the connection.
# CONNECTED state is static, while FAILURE is a method generating a failed
# state with the given reason.

from enum import Enum

class ConnectionState(Enum):
    CONNECTED = ""
    FAILURE = " generic error"
    FAILURE_INVALID_RECIPIENT = " invalid recipient"
    FAILURE_RECIPIENT_NOT_ME = " recipient not me"
    FAILURE_INVALID_CALLER = " invalid caller"

    def __str__(self):
        return ("true" if self == ConnectionState.CONNECTED else "false") + self.value