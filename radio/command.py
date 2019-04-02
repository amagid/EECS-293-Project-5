# The Command Enumeration represents all of the valid commands, and includes a
# method for finding the closest matching Command instance based on a string
# input.

class Command:
    pass
    # TO = "TO"
    # REP = "REP"
    # THISIS = "THISIS"
    # INVALID = None


    # # CLOSEST_MATCH takes a string representation of a command and returns the closest matching Command, or Command.INVALID if 
    # # the raw_command is really far off.
    # CLOSEST_MATCH(raw_command):
    #     initialize a score_dictionary to {
    #         "TO": 0,
    #         "REP": 0,
    #         "THISIS": 0
    #     }
    #     for each entry in the score_dictionary:
    #         Subtract one point for each unit of length difference between the raw command and the key of the entry
    #         Add one point for each letter the key of the entry has in common with the raw command

    #     Return the entry with the highest score. If there is a tie, return INVALID. If no commands have a positive score, return INVALID.

