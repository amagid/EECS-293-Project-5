# The Parser class is responsible for taking the proper-type whole messages
# from the Reader and parsing them into valid-type messages. The scope of the
# Parser is limited to a single message, so it does not verify message order or
# placement in stream.

from radio.reader import Reader

class Parser:
    # INIT method initializes a Reader to be stored internally
    def __init__(self):
        self._reader = Reader()
        self._leftovers = None

    
    # Returns my actual recipient address (SETUP METHOD)
    def recipient_address(self):
        return self._reader.recipient_address()


    # Returns the actual caller address (DEBUG METHOD)
    def caller_address(self):
        return self._reader.caller_address()

    
    # Returns the next whole message as an instance of the Message class
    def next_message():
        message = self._reader.next_message()
        command, value = self._extract_command_and_value(message)
        return Message(command, value)

    
    # Reads a single raw message string and returns the command and value as best it can
    def _extract_command_and_value(message):
        number_start_index = self._first_digit_index(message)
        raw_command = message_chunks[:number_start_index]
        raw_value = message_chunks[number_start_index:]

        command = Command.closest_match(raw_command)
        value, leftovers = self._clean_value(raw_value)

        self._leftovers = leftovers
        return command, value

    def _first_digit_index(message):
        for index in range(len(message)):
            if message[index].isdigit():
                return index

    
    # Parses a potential value, separates and returns the first "good" value it sees as well as the leftovers
    def _clean_value(raw_value):
        value_string = ""
        found_number = False
        final_index = -1
        for index in range(len(raw_value)):
            if raw_value[index].isdigit():
                value_string += raw_value[index]
                found_number = True
                final_index = index
            elif found_number:
                break

        value = int(value_string)
        leftovers = raw_value[final_index+1:]
        return value, leftovers

