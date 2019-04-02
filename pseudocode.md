## Purpose

The purpose of this project is to read simulated radio connection input from a file and decide whether or not it can connect to the "caller" with the given information.

## Error Handling Approach

On a basic level, there are three layers to the system: Radio, Parser, and Reader. Parser and Reader form a barricade against invalid input, with Reader handling missing and wrong-type input and Parser handling poorly formatted but correct-type inputs. This allows Radio to simply take exclusively valid input and only handle high-level protocol errors, such as messages coming in the incorrect order.

The Parser and Reader assume that some degree of incorrectness is acceptable for improved robustness. Therefore, there are some cases where a "best guess" is made when receiving garbled input. If the guess is above a certain reliability threshold, it is returned as absolutely VALID. If not, it is stated as absolutely INVALID. This essentially makes a preference for robustness over correctness.

Errors are almost entirely handled locally by each class to keep the parts of the program appropriately modular. Each successive module of the program simply asserts that the previous module has done its job in processing the input. That is, Radio asserts that it only receives Message objects and handles high-level protocol issues itself. Parser asserts that it only receives input that exists and is of the correct type and internally handles improperly formatted or garbled messages. Reader is on the front-lines, and therefore makes no assertions, and internally handles all input type issues. These layers of assertions also help to ensure each successive class is operating properly to its specification, as it will fail loudly if not.

To address the concerns of attackers gleaning useful information about the internal workings of the program through error messages, the only returns of the system are a connection state and a vague reason such as "invalid caller" or "invalid recipient". The program implements a centralized backup for unexpected error handling at the top level. This is achieved since the program's main method, Radio.ATTEMPT_CONNECT(), surrounds its entire content in a try-catch. If a static DEBUG flag is true, any caught errors will be returned. If it is false, the caught errors will be logged quietly and swallowed. This way, no raw exceptions are ever returned to the client when in production.

## Classes

#### Reader

The Reader class is responsible for reading inputs from the input stream and ensuring they are of the correct type and exist before passing them to the Parser.

```py
class Reader:

    # Initializer connects the Reader to standard input
    INIT():
        store input stream in self._input
        store caller address in self._caller_address
        store recipient address in self._recipient_address


    # Return the actual recipient address (SETUP METHOD)
    RECIPIENT_ADDRESS():
        return self._recipient_address


    # Return the actual caller address (DEBUG METHOD)
    CALLER_ADDRESS():
        return self._caller_address

    
    # NEXT_MESSAGE is responsible for retrieving the next whole message
    # Returns None if we are at the end of the stream
    # Makes no promises about the formatting of a message - simply ensures the message is of the correct data type and exists
    NEXT_MESSAGE():
        initialize string output to empty string
        if _NEXT_CHARACTER() is not a newline:
            append _NEXT_CHARACTER() to output string

        return output string


    # _NEXT_CHARACTER is an internal method responsible for reading the next character from the input stream
    # Returns None if there is no next character
    _NEXT_CHARACTER():
        if _INPUT_STREAM_VALID():
            return next character from input stream
        else:
            return None


    # _INPUT_STREAM_VALID detecs whether the input stream is still valid
    _INPUT_STREAM_VALID():
        return True if input stream is still open and has more characters in it
```

#### Parser

The Parser class is responsible for taking the proper-type whole messages from the Reader and parsing them into valid-type messages. The scope of the Parser is limited to a single message, so it does not verify message order or placement in stream.

```py
class Parser:

    # INIT method initializes a Reader to be stored internally
    INIT():
        initialize a Reader and store it in self._reader
        initialize self._leftovers to None

    
    # Returns my actual recipient address (SETUP METHOD)
    RECIPIENT_ADDRESS():
        return self._reader.RECIPIENT_ADDRESS()


    # Returns the actual caller address (DEBUG METHOD)
    CALLER_ADDRESS():
        return self._reader.CALLER_ADDRESS()

    
    # Returns the next whole message as an instance of the Message class
    NEXT_MESSAGE():
        store self._reader.NEXT_MESSAGE in message variable
        store _EXTRACT_COMMAND_AND_VALUE(message) in command, value
        generate Message instance from command and value inputs
        return generated Message instance

    
    # Reads a single raw message string and returns the command and value as best it can
    _EXTRACT_COMMAND_AND_VALUE(message):
        split message on space delimiter and store in raw_command and raw_value
        store Command.CLOSEST_MATCH(raw_command) in command
        store _CLEAN_VALUE(raw_value) in value, leftovers
        store leftovers in _leftovers
        return command, value

    
    # Parses a potential value, separates and returns the first "good" value it sees as well as the leftovers
    _CLEAN_VALUE(raw_value):
        iterate through string until digits found
        store read digits as a number in value
        store remainder of message to right of value in leftovers
        return value, leftovers
```

#### Message

The Message class represents a cleaned and parsed single message, containing a command and a value.

```py
class Message:

    # The static INVALID Message instance is used for any message that cannot be parsed reliably
    INVALID = Message(None, None)

    # The INIT method takes a Command instance and a numerical value and stores them
    INIT(command, value):
        store command in self._command
        store value in self._value


    # Builds a new Message instance. Returns the INVALID instance if the given inputs are invalid
    BUILD(command, value):
        if command or value is None, return the INVALID Message instance.
        else return a newly initialized Message


    # Retrieve the stored Command
    COMMAND():
        return self._command


    # Retrive the stored Value
    VALUE():
        return self._value


    # Check whether or not this Message is valid
    IS_VALID():
        return self != INVALID Message instance
```

#### Command (Enum)

The Command Enumeration represents all of the valid commands, and includes a method for finding the closest matching Command instance based on a string input.

```py
enum Command:
    
    TO = "TO"
    REP = "REP"
    THISIS = "THISIS"
    INVALID = None


    # CLOSEST_MATCH takes a string representation of a command and returns the closest matching Command, or Command.INVALID if 
    # the raw_command is really far off.
    CLOSEST_MATCH(raw_command):
        initialize a score_dictionary to {
            "TO": 0,
            "REP": 0,
            "THISIS": 0
        }
        for each entry in the score_dictionary:
            Subtract one point for each unit of length difference between the raw command and the key of the entry
            Add one point for each letter the key of the entry has in common with the raw command

        Return the entry with the highest score. If there is a tie, return INVALID. If no commands have a positive score, return INVALID.
```

#### Radio

The Radio class is the master class of the program. It initializes an internally stored Parser and uses it to read valid, sanitized Messages from the input stream. It is responsible only for handling high-level protocol errors, and expects that all received Messages will be correctly formatted and exist, or otherwise be marked as INVALID.

```py
class Radio:

    # Controls whether or not exceptions are returned
    DEBUG = False

    # INIT initializes this Radio with an internal Parser
    INIT():
        initialize a Parser and store it in self._parser
        initialize self._to_address to None
        initialize self._from_address to None 
        initialize self._command_parsers to a dictionary containing {
            Message.TO = self._PARSE_TO,
            Message.REP = self._PARSE_LONE_REP,
            Message.THISIS = self._PARSE_THISIS,
            Message.INVALID = self._PARSE_INVALID
        }

    
    # ATTEMPT_CONNECT is the main method. Reads messages one at a time and parses major message sections based on the received
    # message. Reading a message of a particular type kicks off parsing further for that type of message.
    # This method also swallows all exceptions when in production to ensure no raw errors ever make it back to the client.
    ATTEMPT_CONNECT():
        try:
            store self._parser.NEXT_MESSAGE() in message
            while message is not None and not CONNECTION_VALID():
                read message.Command and run associated parser stored in self._command_parsers

            initialize connection_state
            if CONNECTION_VALID():
                store ConnectionState.CONNECTED in connection_state
            else:
                store _FAILED_CONNECTION_STATE() in connection_state

            return string representation of connection_state
        catch Exception e:
            if not DEBUG:
                return string representation of generic FAILURE ConnectionState
            else:
                return string representation of received error


    # CONNECTION_VALID is a public method returning whether or not the connection is currently valid
    CONNECTION_VALID():
        return True if self._to_address is equal to self._parser.RECIPIENT_ADDRESS() and self._from_address is a valid number equal to self._parser.CALLER_ADDRESS()


    # _FAILED_CONNECTION_STATE returns the proper failure ConnectionState based on the current state information
    _FAILED_CONNECTION_STATE():
        initialize error to _CHECK_RECIPIENT_ERROR()
        if error is None
            set error to _CHECK_CALLER_ERROR()
        if error is still None
            set error to ConnectionState.FAILURE

        return error


    # _CHECK_RECIPIENT_ERROR returns the appropriate RECIPIENT_ERROR ConnectionState based on the current state information
    # Returns None if there is no issue with the recipient information
    _CHECK_RECIPIENT_ERROR():
        if self._to_address is invalid or missing, return ConnectionState.FAILURE_INVALID_RECIPIENT
        elif self._to_address is valid but not my address, return ConnectionState.FAILURE_RECIPIENT_NOT_ME
        else return None


    # _CHECK_CALLER_ERROR returns the appropriate CALLER_ERROR ConnectionState based on the current state information
    # Returns None if there is no issue with the caller information
    _CHECK_CALLER_ERROR():
        if self._from_address is invalid or missing, return ConnectionState.FAILURE_INVALID_CALLER
        else return None
```

#### ConnectionState (Enum)

The ConnectionState class represents the current state of the connection. CONNECTED state is static, while FAILURE is a method generating a failed state with the given reason.

```py
enum ConnectionState:
    CONNECTED = ""
    FAILURE = " generic error"
    FAILURE_INVALID_RECIPIENT = " invalid recipient"
    FAILURE_RECIPIENT_NOT_ME = " recipient not me"
    FAILURE_INVALID_CALLER = " invalid caller"

    TO_STRING():
        initialize output to empty string
        if self is ConnectionState.CONNECTED, append "true" to output
        else append "false" to output
        append enum instance value to output
```
